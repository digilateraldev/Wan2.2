from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import subprocess
import os
from typing import Optional
from pathlib import Path
import shutil
import uuid

app = FastAPI()

BASE_DIR = Path(__file__).parent
REPO_DIR_PARENT=BASE_DIR.parent
REPO_DIR = REPO_DIR_PARENT / "Wan2.2"
WEIGHTS_DIR = BASE_DIR / "Wan2.2-Animate-14B"
PROCESS_WEIGHTS_DIR=WEIGHTS_DIR / "process_checkpoint"
PREPROCESS_SCRIPT = REPO_DIR / "wan" / "modules" / "animate" / "preprocess" / "preprocess_data.py"
GENERATE_SCRIPT = REPO_DIR / "generate.py"
WORK_DIR = BASE_DIR / "runtime"
DEFAULT_VIDEO_PATH='5secvideo.mp4'
WORK_DIR.mkdir(exist_ok=True)
PYTHON_PATH='/home/digi/miniconda3/envs/wan-animate/bin/python'
@app.post("/animate")
async def animate(image: UploadFile = File(...), video: Optional[UploadFile] = File(None)):
    job_id = str(uuid.uuid4())
    job_folder = WORK_DIR / job_id
    job_folder.mkdir(parents=True, exist_ok=True)

    # Save uploaded files
    input_image = job_folder / image.filename
    with open(input_image, "wb") as f:
        f.write(await image.read())

    # Handle optional video
    if video and video.filename:
        input_video = job_folder / video.filename
        with open(input_video, "wb") as f:
            f.write(await video.read())
    else:
        input_video = DEFAULT_VIDEO_PATH  # fallback to default
    # Preprocess output directory
    preprocess_out = job_folder / "process_results"
    preprocess_out.mkdir()

    # Run preprocessing
    subprocess.run([
        str(PYTHON_PATH), str(PREPROCESS_SCRIPT),
        "--ckpt_path", str(PROCESS_WEIGHTS_DIR),
        "--video_path", str(input_video),
        "--refer_path", str(input_image),
        "--save_path", str(preprocess_out),
        "--resolution_area", "1280", "720",
        "--retarget_flag",
        # "--use_flux" #DONT FORGET TO UNCOMMENT THIS ON PROD
    ], check=True)

    # Define output directory for final generated video
    output_dir = job_folder / "output"
    output_dir.mkdir(exist_ok=True)
    output_file=os.path.join(output_dir,'generated_video.mp4')
    # Run generate.py with explicit output path
    subprocess.run([
        str(PYTHON_PATH), str(GENERATE_SCRIPT),
        "--task", "animate-14B",
        "--ckpt_dir", str(WEIGHTS_DIR),
        "--src_root_path", str(preprocess_out),
        "--refert_num", "1",
        "--save_file", str(output_file),
        "--offload_model", "True"
    ], check=True)

    # Now output_dir contains only generated files → safe to pick final .mp4
    # result_videos = list(output_dir.glob("*.mp4"))
    # if not result_videos:
    #     return {"error": "Model did not produce an output video"}

    final_video = output_file

    return FileResponse(str(final_video), media_type="video/mp4", filename="result.mp4")
