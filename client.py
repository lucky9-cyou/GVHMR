from gradio_client import Client, handle_file
import bvh

client = Client("http://127.0.0.1:7861/")
result = client.predict(
    video_path={"video": handle_file("docs/example_video/hugo.mp4")}, cam_status="Static Camera", api_name="/predict"
)

incam_out = "incam.bvh"
global_out = "global.bvh"

bvh.save(incam_out, result[2])
bvh.save(global_out, result[3])
