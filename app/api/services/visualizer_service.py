"""Visualizer Service."""
import logging
from collections import defaultdict

import cv2
import numpy as np
from ultralytics import YOLO

from app.api.helpers.constants import YOLOV8_CLASSES
from app.core.config import TRITON_SERVER_URL

logger = logging.getLogger(__name__)


class VisualizerService:
    """Visualizer Service."""

    def __init__(self) -> None:
        """Initialize Visualizer Service."""
        # self.triton_client = InferenceServerClient(TRITON_SERVER_URL)

    def detect_label_from_video(self, video_path: str):
        """Detect Label from Video."""
        video = cv2.VideoCapture(video_path)
        client = YOLO(f"grpc://{TRITON_SERVER_URL}/label_detection", task="detect")
        class_time_map = defaultdict(list)
        while True:
            ret, frame = video.read()
            if not ret:
                break

            predictions = self._infer_triton(frame, client)
            classes = list(set(predictions.boxes.cls.to(int).tolist()))
            classes = [YOLOV8_CLASSES[x] for x in classes]

            # get video current time
            current_time = video.get(cv2.CAP_PROP_POS_MSEC) / 1000

            # add current time to class time map and merge if the previous time to current time is less than 10 seconds
            for class_name in classes:
                if len(class_time_map[class_name]) > 0 and class_time_map[class_name][-1] - current_time < 10:
                    class_time_map[class_name][-1] = current_time
                else:
                    class_time_map[class_name].append(current_time)

        # Release video
        video.release()
        cv2.destroyAllWindows()

        return class_time_map

    def _infer_triton(self, frame: np.ndarray, client):
        """Triton Inference."""
        results = client.predict(frame, imgsz=[224, 224])[0]
        logger.info(results)
        return results
