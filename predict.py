# Prediction interface for Cog ⚙️
# https://github.com/replicate/cog/blob/main/docs/python.md

from cog import BasePredictor, Input, Path
import os
import sys
import time
import subprocess

class Predictor(BasePredictor):
    def setup(self) -> None:
        """Load the model into memory to make running multiple predictions efficient"""
        # Link /src/checkpoints to /InterpAny/checkpoints
        os.system("ln -s /src/checkpoints /InterpAny/checkpoints")

    def predict(
        self,
        video: Path = Input(description="Input video"),
        num: int = Input(
            description="number of extracted images", ge=0, le=10, default=3
        ),
        fps: int = Input(
            description="Fps of the output video. Leave blank to keep the same fps", default=15
        )
    ) -> Path:
        """Run a single prediction on the model"""
        # Script inference_video needs calls chdir, so need to be relative
        os.chdir('/InterpAny/')

        print("Input file path: " + str(video))
        # get filname of video file and remove first 3 characters of filename
        filename = os.path.basename(video) 
        filename = filename[3:]
        print(filename)

        # Clean up past runs (just in case)
        output_dir = "./results/video_results/"
        os.system("rm -rf " + output_dir)
        os.system("mkdir -p " + output_dir)

        command = [
            "python", "inference_video.py",
            "--video", str(video),
            "--model", "RIFE",
            "--variant", "DR",
            "--checkpoint", "/InterpAny/checkpoints/RIFE/DR-RIFE-pro/",
            "--save_dir", "./results/video_results/",
            "--num", str(num),
        ]
        if fps is not None:
            command.extend(["--fps", str(fps)])

        # Call command and log output
        print("Running subprocess command")
        subprocess.run(command)
        print("Finished subprocess command")
        output_path = "/InterpAny/results/video_results/" + filename

        # convert mp4 in output_path with ffmpeg
        os.system("ffmpeg -y -i " + output_path + " -vcodec libx264 /tmp/output.mp4")
        return Path("/tmp/output.mp4")        
