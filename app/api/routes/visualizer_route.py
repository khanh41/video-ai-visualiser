from multiprocessing import Pool
from os import cpu_count

from fastapi import APIRouter, File, UploadFile, Depends
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader
from loguru import logger

from app.api.helpers.utils import save_and_split_video
from app.api.responses.base import BaseResponse
from app.api.responses.visualizer_response import ListLabelDetectionResponse, LabelDetectionResponse
from app.api.services.visualizer_service import VisualizerService
from app.core.config import API_KEY

api_key_header = APIKeyHeader(name="X-API-Key")
router = APIRouter()
visualizer_service = VisualizerService()


def verify_api_key(x_api_key: str = Security(api_key_header)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")


@router.post(
    "/label-detection",
    response_description="Detect label from video file",
    response_model=BaseResponse[ListLabelDetectionResponse],
)
async def detect_label_from_video_file(
    video_file: UploadFile = File(...),
    verify=Depends(verify_api_key),
):
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
    segment_time = 60
    split_paths = await save_and_split_video(video_file, segment_time=segment_time)

    # Detect label from video file
    with Pool(processes=cpu_count()) as pool:
        params = [(split_path, segment_time * index) for index, split_path in enumerate(split_paths)]
        _detections = pool.starmap(visualizer_service.detect_label_from_video, params)

    detections: list[LabelDetectionResponse] = []
    for detection in _detections:
        detections.extend(detection)

    # Sort the detections by start time
    detections = sorted(detections, key=lambda x: x.start_time)
    logger.info(f"Detected labels: {detections}")

    return BaseResponse(
        success=True,
        status_code=200,
        message="Label detected",
        data=ListLabelDetectionResponse(detections=detections),
    )
