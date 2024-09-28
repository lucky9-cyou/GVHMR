import gradio as gr

from omegaconf import OmegaConf

from app.demo import *


def prepare_cfg(is_static:bool, video_path:str, demo_id:str):
    output_root = Path(video_path).parent / 'output'
    output_root = str(output_root.absolute())

    # Cfg
    with initialize_config_module(version_base="1.3", config_module=f"hmr4d.configs"):
        overrides = [
            f"video_name={demo_id}",
            f"static_cam={is_static}",
            f"verbose={False}",
        ]

        # Allow to change output root
        overrides.append(f"output_root={output_root}")
        register_store_gvhmr()
        cfg = compose(config_name="demo", overrides=overrides)

    # Output
    Log.info(f"[Output Dir]: {cfg.output_dir}")
    Path(cfg.output_dir).mkdir(parents=True, exist_ok=True)
    Path(cfg.preprocess_dir).mkdir(parents=True, exist_ok=True)

    # Copy raw-input-video to video_path
    Log.info(f"[Copy Video] {video_path} -> {cfg.video_path}")
    if not Path(cfg.video_path).exists() or get_video_lwh(video_path)[0] != get_video_lwh(cfg.video_path)[0]:
        reader = get_video_reader(video_path)
        writer = get_writer(cfg.video_path, fps=30, crf=CRF)
        for img in tqdm(reader, total=get_video_lwh(video_path)[0], desc=f"Copy"):
            writer.write_frame(img)
        writer.close()
        reader.close()

    return cfg


def run_demo(cfg, progress):
    ''' Allow user to adjust GPU quota. '''

    smpl_utils = {
            'smplx'       : make_smplx("supermotion"),
            'J_regressor' : torch.load("hmr4d/utils/body_model/smpl_neutral_J_regressor.pt"),
            'smplx2smpl'  : torch.load("hmr4d/utils/body_model/smplx2smpl_sparse.pt"),
            'faces_smpl'  : make_smplx("smpl").faces,
        }

    def run_GPU_task():
        Log.info(f"[GPU]: {torch.cuda.get_device_name()}")
        Log.info(f'[GPU]: {torch.cuda.get_device_properties("cuda")}')

        # ===== Preprocess and save to disk ===== #
        run_preprocess(cfg, progress)
        data = load_data_dict(cfg)

        # ===== HMR4D ===== #
        Log.info("[HMR4D] Predicting")
        progress(0, '[GVHMR] Initializing pipeline...')
        model: DemoPL = hydra.utils.instantiate(cfg.model, _recursive_=False)
        model.load_pretrained_model(cfg.ckpt_path)
        model = model.eval().cuda()
        tic = Log.sync_time()
        progress(1/3, '[GVHMR] Predicting...')
        pred = model.predict(data, static_cam=cfg.static_cam)
        pred = detach_to_cpu(pred)
        data_time = data["length"] / 30
        Log.info(f"[HMR4D] Elapsed: {Log.sync_time() - tic:.2f}s for data-length={data_time:.1f}s")

        progress(2/3, '[GVHMR] Rendering...')

        # ===== Render ===== #
        smpl_utils['smplx'] = smpl_utils['smplx'].cuda()
        smpl_utils['J_regressor'] = smpl_utils['J_regressor'].cuda()
        smpl_utils['smplx2smpl'] = smpl_utils['smplx2smpl'].cuda()
        render_incam(cfg, pred, smpl_utils)
        render_global(cfg, pred, smpl_utils)
        return

    run_GPU_task()
    return


def handler(video_path, cam_status, progress=gr.Progress()):
    # 0. Check validity of inputs.
    if cam_status not in ['Static Camera', 'Dynamic Camera']:
        raise gr.Error('Please define the camera status!', duration=5)
    if video_path is None or not Path(video_path).exists():
        raise gr.Error('Can not find the video!', duration=5)

    # 1. Deal with APP inputs.
    is_static = cam_status == 'Static Camera'
    Log.info(f"[Input Args] is_static: {is_static}")
    Log.info(f"[Input Args] video_path: {video_path}")

    if not is_static:
        Log.info("[Warning] Dynamic Camera is not supported yet.")
        raise gr.Error('DPVO is not supported in spaces yet. Try to run videos with static camera instead!', duration=20)

    # 2. Prepare cfg.
    Log.info(f"[Video]: {video_path}")
    demo_id = f'{Path(video_path).stem}_{np.random.randint(0, 1024):04d}'
    cfg = prepare_cfg(is_static, video_path, demo_id)

    # 3. Run demo.
    cfg = OmegaConf.to_container(cfg, resolve=True)
    cfg = OmegaConf.create(cfg)
    run_demo(cfg, progress)

    # 4. Prepare the output.
    return cfg.paths.incam_video, cfg.paths.global_video