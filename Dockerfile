FROM pytorch/pytorch:2.4.1-cuda12.1-cudnn9-devel

WORKDIR /gvhmr

COPY requirements.txt .

SHELL ["/bin/bash", "-c"] 
RUN conda init bash
# for environment activation
SHELL ["conda", "run", "-n", "base", "/bin/bash", "-c"]
RUN pip install --extra-index-url https://miropsota.github.io/torch_packages_builder pytorch3d==0.7.8+pt2.4.1cu121 && pip install -r requirements.txt -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple && pip install gradio -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

CMD ["/bin/bash"]