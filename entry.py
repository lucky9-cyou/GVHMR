import os
import gradio as gr

from app.gui import get_inputs_components, get_outputs_components, get_desc
from app.handler import handler


def entry():
    try:
        demo = gr.Interface(
                fn          = handler,
                inputs      = get_inputs_components(),
                outputs     = get_outputs_components(),
            )

        demo.launch()
    except Exception as e:
        print(f'Error: {str(e)}')

if __name__ == '__main__':
    entry()