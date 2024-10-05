import os
import gradio as gr

from app.gui import get_inputs_components, get_outputs_components
from app.handler import handler


def entry():
    REPO_ROOT = str(os.path.join(os.path.dirname(__file__)))
    os.system(f'touch {REPO_ROOT}/server_up')
    os.system('lsof -i :7860 | grep LISTEN | awk \'{print $2}\' | xargs kill')
    
    try:
        demo = gr.Interface(
            fn=handler,
            inputs=get_inputs_components(),
            outputs=get_outputs_components(),
        )

        demo.launch(server_name="0.0.0.0", server_port=12346, share=True)
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    entry()
