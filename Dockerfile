FROM pytorch/pytorch:2.4.1-cuda12.1-cudnn9-devel

WORKDIR /gvhmr

COPY . .

SHELL ["/bin/bash", "-c"] 
RUN conda init bash
# for environment activation
SHELL ["conda", "run", "-n", "base", "/bin/bash", "-c"]
RUN pip install --extra-index-url https://miropsota.github.io/torch_packages_builder pytorch3d==0.7.8+pt2.4.1cu121 && pip install -r requirements.txt -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple && pip install -e . && pip install gradio -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
RUN cd third-party/DPVO && wget https://gitlab.com/libeigen/eigen/-/archive/3.4.0/eigen-3.4.0.zip && unzip eigen-3.4.0.zip -d thirdparty && rm -rf eigen-3.4.0.zip && pip install torch-scatter -f "https://data.pyg.org/whl/torch-2.4.0+cu121.html" && pip install numba pypose -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple && pip install -e .

CMD ["/bin/bash"]