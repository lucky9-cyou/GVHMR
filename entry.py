import os
import gradio as gr

from app.gui import get_inputs_components, get_outputs_components
from app.handler import pose_handler, track_handler

with gr.Blocks(theme=gr.themes.Monochrome()) as iface:
    track_state = gr.State(
        {
            "cfg": None,
            "bbx_xyxys": None,
        }
    )
    with gr.Column():
        # input video
        gr.Markdown("## Step1: Upload video and track")
        with gr.Row():
            with gr.Column():
                video = gr.Video(label="INPUT VIDEO", show_label=True)
                camera_status = gr.Radio(
                    choices=["Static Camera", "Dynamic Camera"],
                    label="Camera Status",
                    info="If the camera is static, DPVO will be skipped.",
                )
                track_button = gr.Button(value="Track")
            with gr.Column():
                track_video = gr.Video(label="TRACKED VIDEO", show_label=True)
                track_id = gr.Number(label="Track ID", show_label=True)
                gvhmr = gr.Button(value="GVHMR")
        with gr.Row():
            incam_result = gr.PlayableVideo(
                label="INCAM RESULT",
                show_label=True,
            )
            global_result = gr.PlayableVideo(
                label="GLOBAL RESULT",
                show_label=True,
            )            
        with gr.Row():
            bvh_incam_result = gr.File(
                label="BVH INCAM JSON RESULT",
                show_label=True,
            )
            bvh_global_result = gr.File(
                label="BVH GLOBAL JSON RESULT",
                show_label=True,
            )
        with gr.Row():
            bvh_incam = gr.File(
                label="BVH INCAM RESULT",
                show_label=True,
            )
            bvh_global = gr.File(
                label="BVH GLOBAL RESULT",
                show_label=True,
            )
        with gr.Row():
            ground = gr.File(
                label="Ground Parameters",
                show_label=True,
            )
            mesh = gr.File(
                label="First Mesh",
                show_label=True,
            )
    
    track_button.click(track_handler, [video, camera_status], [track_state, track_video])
    gvhmr.click(pose_handler, [video, track_state, track_id], [incam_result, global_result, bvh_incam_result, bvh_global_result, bvh_incam, bvh_global, ground, mesh])

iface.launch(debug=True, server_name="0.0.0.0", server_port=6006)