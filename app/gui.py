import os
import gradio as gr
from glob import glob


def get_inputs_components():
    return [
        gr.Video(
            label="INPUT VIDEO",
            show_label=True,
        ),
        gr.Radio(
            choices=["Static Camera", "Dynamic Camera"],
            label="Camera Status",
            info="If the camera is static, DPVO will be skipped.",
        ),
    ]


def get_outputs_components():
    return [
        gr.PlayableVideo(
            label="INCAM RESULT",
            show_label=True,
        ),
        gr.PlayableVideo(
            label="GLOBAL RESULT",
            show_label=True,
        ),
        gr.File(
            label="BVH INCAM JSON RESULT",
            show_label=True,
        ),
        gr.File(
            label="BVH GLOBAL JSON RESULT",
            show_label=True,
        ),
        gr.File(
            label="BVH INCAM RESULT",
            show_label=True,
        ),
        gr.File(
            label="BVH GLOBAL RESULT",
            show_label=True,
        ),
        gr.File(
            label="Ground Parameters",
            show_label=True,
        ),
        gr.File(
            label="First Mesh",
            show_label=True,
        ),
    ]
