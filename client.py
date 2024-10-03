from gradio_client import Client, handle_file
import bvh
import argparse
import os
import json
import wget

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Client for BVH")
    parser.add_argument("--video", type=str, required=True, help="Path to the video")
    parser.add_argument("--output", type=str, default="output", help="Path to the output")
    parser.add_argument("--server_address", type=str, default="http://10.26.1.168:12346/", help="Camera status")

    args = parser.parse_args()
    
    if not os.path.exists(args.output):
        os.makedirs(args.output, exist_ok=True)
    
    client = Client(args.server_address)
    result = client.predict(
        video_path={"video": handle_file(args.video)}, cam_status="Static Camera", api_name="/predict"
    )
    
    incam_out = args.output + "/incam.bvh"
    global_out = args.output + "/global.bvh"
    
    wget.download(args.server_address + 'file=' + result[2], args.output + "/incam.json")
    wget.download(args.server_address + 'file=' + result[3], args.output + "/global.json")
    wget.download(args.server_address + 'file=' + result[4], args.output + "/ground.json")
    
    incam = json.load(open(args.output + "/incam.json"))
    global_ = json.load(open(args.output + "/global.json"))
    
    bvh.save(incam_out, incam)
    bvh.save(global_out, global_)
