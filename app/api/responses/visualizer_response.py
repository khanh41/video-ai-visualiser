"""Visualizer Response."""
from pydantic import BaseModel, Field


class LabelDetectionResponse(BaseModel):
    """Response model for label detection."""
    label: str = Field(description="Label of the visualizer")
    confidence_threshold: float = Field(description="Confidence threshold")
    start_time: float = Field(description="Start time of the visualizer")
    end_time: float = Field(description="End time of the visualizer")


class ListLabelDetectionResponse(BaseModel):
    """Response model for list label detection."""
    detections: list[LabelDetectionResponse] = Field(description="List of label detection")
