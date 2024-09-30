FROM pytorch/pytorch:2.4.1-cuda12.1-cudnn9-devel

RUN apt update && apt install -y wget unzip libgl1-mesa-glx libglib2.0-dev git ffmpeg 

SHELL ["/bin/bash", "-c"] 
RUN conda init bash
# for environment activation
SHELL ["conda", "run", "-n", "base", "/bin/bash", "-c"]

RUN pip install --extra-index-url https://miropsota.github.io/torch_packages_builder pytorch3d==0.7.8+pt2.4.1cu121 && pip install timm==0.9.12 lightning==2.3.0 hydra-core==1.3 hydra-zen hydra_colorlog rich numpy==1.23.5 jupyter matplotlib ipdb setuptools>=68.0 black tensorboardX opencv-python ffmpeg-python scikit-image termcolor einops imageio==2.34.1 av joblib trimesh smplx wis3d ultralytics==8.2.42 cython_bbox lapx yacs -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple && pip install gradio smplx[all] -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple && pip install torch-scatter -f "https://data.pyg.org/whl/torch-2.4.0+cu121.html" && pip install numba pypose -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple && pip install git+https://github.com/mattloper/chumpy@9b045ff5d6588a24a0bab52c83f032e2ba433e17

WORKDIR /gvhmr
COPY . .

RUN pip install -e .

ENV CUDA_HOME=/usr/local/cuda-12.1/
ENV PATH=$PATH:/usr/local/cuda-12.1/bin/
ENV TORCH_CUDA_ARCH_LIST="8.9"

# for dpvo
RUN cd third-party/DPVO && wget https://gitlab.com/libeigen/eigen/-/archive/3.4.0/eigen-3.4.0.zip && unzip eigen-3.4.0.zip -d thirdparty && rm -rf eigen-3.4.0.zip
RUN cd third-party/DPVO && pip install -e .

CMD ["python", "entry.py"]