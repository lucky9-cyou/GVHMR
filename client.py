from gradio_client import Client, handle_file
import bvh
import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Client for BVH")
    parser.add_argument("--video", type=str, required=True, help="Path to the video")
    parser.add_argument("--output", type=str, default="output", help="Path to the output")
    parser.add_argument("--server_address", type=str, default="http://10.26.1.168:12345/", help="Camera status")

    args = parser.parse_args()
    
    if not os.path.exists(args.output):
        os.makedirs(args.output, exist_ok=True)
    
    client = Client(args.server_address)
    result = client.predict(
        video_path={"video": handle_file(args.video)}, cam_status="Static Camera", api_name="/predict"
    )

    incam_out = args.output + "/incam.bvh"
    global_out = args.output + "/global.bvh"

    bvh.save(incam_out, result[2])
    bvh.save(global_out, result[3])
