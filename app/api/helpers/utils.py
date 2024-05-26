"""Utils."""
import functools
import os
import subprocess
import time
import uuid
from typing import Any, Callable, TypeVar

import aiofiles
from fastapi import UploadFile, HTTPException
from loguru import logger

F = TypeVar("F", bound=Callable[..., Any])


def calculate_time(func: F) -> F:
    """Calculate time."""

    @functools.wraps(func)
    def inner(*args, **kwargs):
        """Inner function."""
        begin = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        logger.info("Total time taken in %s: %s", func.__qualname__, end - begin)
        return result

    return inner


@calculate_time
async def save_and_split_video(video_file: UploadFile, segment_time: int = 120):
    """Split the video into segments using ffmpeg."""
    # Save the uploaded video file to a temporary location
    temp_dir = "/tmp"
    input_video_path = os.path.join(temp_dir, f"{uuid.uuid4()}.mp4")

    async with aiofiles.open(input_video_path, 'wb') as out_file:
        content = await video_file.read()
        await out_file.write(content)

    # Generate output file template
    output_template = os.path.join(temp_dir, f"{uuid.uuid4()}_%03d.mp4")

    # Split the video using ffmpeg
    try:
        ffmpeg_command = [
            "ffmpeg", "-i", input_video_path, "-c", "copy", "-map", "0",
            "-segment_time", str(segment_time), "-f", "segment", output_template
        ]
        subprocess.run(ffmpeg_command, check=True)
    except subprocess.CalledProcessError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error splitting video: {str(e)}"
        )

    # Clean up the input video file
    os.remove(input_video_path)

    # Collect the paths of the output video segments
    output_files = sorted(
        [f for f in os.listdir(temp_dir) if f.startswith(output_template.split("/")[-1].split("_")[0])]
    )
    output_paths = [os.path.join(temp_dir, f) for f in output_files]

    return output_paths
