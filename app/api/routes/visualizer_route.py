"""Chat route."""
import logging

from fastapi import APIRouter, File
from fastapi import UploadFile

from app.api.helpers.utils import save_and_split_video
from app.api.responses.base import BaseResponse
from app.api.services.visualizer_service import VisualizerService

logger = logging.getLogger(__name__)

router = APIRouter()
visualizer_service = VisualizerService()


@router.post("/label-detection", response_description="Detect label from video file", response_model=BaseResponse)
async def detect_label_from_video_file(video_file: UploadFile = File(...)):
    """Detect label from video file."""
    # Check if the video file is valid
    if not video_file.content_type.startswith("video"):
        return BaseResponse(
            success=False,
            status_code=400,
            message="Invalid video file",
            data=None,
        )

    # Split the video into segments using ffmpeg
    split_paths = await save_and_split_video(video_file)
    for split_path in split_paths:
        visualizer_service.detect_label_from_video(split_path)

    # Detect label from video file

    return BaseResponse(
        success=True,
        status_code=200,
        message="Label detected",
        data=None,
    )
