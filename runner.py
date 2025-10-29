import os



from PIL import Image
img=Image.open('./examples/wan_animate/animate/arif-pose.png')
width, height = img.size
print(width,height)

os.system(f'python3 ./wan/modules/animate/preprocess/preprocess_data.py --ckpt_path ./Wan2.2-Animate-14B/process_checkpoint --video_path ./examples/wan_animate/animate/start_1min.mp4 --refer_path ./examples/wan_animate/animate/arif-pose.png --save_path ./examples/wan_animate/animate/process_results --resolution_area {width} {height} --retarget_flag --use_flux')

pwd=os.system('pwd')
print(f'src_root_path={pwd}/examples/wan_animate/animate/process_results/')
os.system(f'python3 generate.py --task animate-14B --ckpt_dir ./Wan2.2-Animate-14B/ --src_root_path {pwd}/examples/wan_animate/animate/process_results/ --refert_num 1')





