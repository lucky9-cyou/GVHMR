aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://hf-mirror.com/camenduru/SMPLer-X/resolve/main/SMPL_NEUTRAL.pkl -d inputs/checkpoints/body_models/smpl -o SMPL_NEUTRAL.pkl
aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://hf-mirror.com/camenduru/SMPLer-X/resolve/main/SMPLX_NEUTRAL.npz -d inputs/checkpoints/body_models/smplx -o SMPLX_NEUTRAL.npz
aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://hf-mirror.com/camenduru/GVHMR/resolve/main/dpvo/dpvo.pth -d inputs/checkpoints/dpvo -o dpvo.pth
aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://hf-mirror.com/camenduru/GVHMR/resolve/main/gvhmr/gvhmr_siga24_release.ckpt -d inputs/checkpoints/gvhmr -o gvhmr_siga24_release.ckpt
aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://hf-mirror.com/camenduru/GVHMR/resolve/main/hmr2/epoch%3D10-step%3D25000.ckpt -d inputs/checkpoints/hmr2 -o epoch=10-step=25000.ckpt
aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://hf-mirror.com/camenduru/GVHMR/resolve/main/vitpose/vitpose-h-multi-coco.pth -d inputs/checkpoints/vitpose -o vitpose-h-multi-coco.pth
aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://hf-mirror.com/camenduru/GVHMR/resolve/main/yolo/yolov8x.pt -d inputs/checkpoints/yolo -o yolov8x.pt
