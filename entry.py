import os
import gradio as gr

from app.gui import get_inputs_components, get_outputs_components
from app.handler import handler


def entry():
    try:
        demo = gr.Interface(
            fn=handler,
            inputs=get_inputs_components(),
            outputs=get_outputs_components(),
        )

        demo.launch(server_name="0.0.0.0", server_port=12345, share=True)
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    entry()
