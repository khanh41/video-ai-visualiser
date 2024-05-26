"""Visualizer Service."""
from collections import defaultdict

import cv2
import numpy as np
from loguru import logger
from ultralytics import YOLO

from app.api.helpers.constants import YOLOV8_CLASSES
from app.api.responses.visualizer_response import LabelDetectionResponse
from app.core.config import TRITON_SERVER_URL


class VisualizerService:
    """Visualizer Service."""

    def __init__(self) -> None:
        """Initialize Visualizer Service."""
        # self.triton_client = InferenceServerClient(TRITON_SERVER_URL)

    def detect_label_from_video(self, video_path: str, initial_time: float) -> list[LabelDetectionResponse]:
        """Detect Label from Video."""
        video = cv2.VideoCapture(video_path)
        client = YOLO(f"grpc://{TRITON_SERVER_URL}/label_detection", task="detect")
        class_time_map: dict[str, list[LabelDetectionResponse]] = defaultdict(list)
        while True:
            ret, frame = video.read()
            if not ret:
                break

            predictions = self._infer_triton(frame, client)
            classes = list(set(predictions.boxes.cls.to(int).tolist()))
            classes = [YOLOV8_CLASSES[x] for x in classes]

            # get video current time
            current_time = video.get(cv2.CAP_PROP_POS_MSEC) / 1000
            current_time += initial_time

            # add current time to class time map and merge if the previous time to current time is less than 10 seconds
            for class_name in classes:
                if len(class_time_map[class_name]) > 0 and class_time_map[class_name][-1].end_time - current_time < 10:
                    class_time_map[class_name][-1].end_time = current_time
                else:
                    response = LabelDetectionResponse(
                        label=class_name,
                        confidence_threshold=1,
                        start_time=current_time,
                        end_time=current_time,
                    )
                    class_time_map[class_name].append(response)
                    logger.info(f"Added {class_name} from {current_time}")

        # Release video
        video.release()
        cv2.destroyAllWindows()

        detections = []
        for class_name, class_time_list in class_time_map.items():
            detections.extend(class_time_list)

        return sorted(detections, key=lambda x: x.start_time)

    def _infer_triton(self, frame: np.ndarray, client):
        """Triton Inference."""
        results = client.predict(frame, imgsz=[224, 224], verbose=False)[0]
        return results
