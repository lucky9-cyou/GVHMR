from gradio_client import Client, handle_file

client = Client("http://127.0.0.1:7861/")
result = client.predict(
    video_path={"video": handle_file("docs/example_video/hugo.mp4")}, cam_status="Static Camera", api_name="/predict"
)

print(result)
