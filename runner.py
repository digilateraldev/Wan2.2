import os
from PIL import Image
import argparse
from datetime import datetime

# Get the current datetime object
now = datetime.now()

# Format the datetime object into a string suitable for a filename
# Common format: YearMonthDay-HourMinuteSecond
timestamp_str = now.strftime("%Y%m%d-%H%M%S")

# Construct the filename
processing_dir = f"./wan/process_results_{timestamp_str}"
parser = argparse.ArgumentParser(description="Generate animation from a video and image using the Wan 2.2 animate")
parser.add_argument('input_image_path',type=str, help="Path to the input photo file." )
parser.add_argument('input_video_path',type=str, help="Path to the input video file.")
args=parser.parse_args()
# args.input_image_path
img=Image.open(args.input_image_path)
width, height = img.size
print(width,height)
os.system(f'python3 ./wan/modules/animate/preprocess/preprocess_data.py --ckpt_path ./Wan2.2-Animate-14B/process_checkpoint --video_path ./examples/wan_animate/animate/{args.input_video_path} --refer_path ./examples/wan_animate/animate/{args.input_image_path} --save_path {processing_dir} --resolution_area {width} {height} --retarget_flag --use_flux')
os.system(f'python3 generate.py --task animate-14B --ckpt_dir ./Wan2.2-Animate-14B/ --src_root_path {processing_dir} --refert_num 1 --offload_model True')
