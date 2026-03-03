"""
Pydantic DTOs für API-Responses
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class DetectedBoxResponse(BaseModel):
    """DTO für eine erkannte Box"""
    id: int
    x1: float
    y1: float
    x2: float
    y2: float
    confidence: float
    class_id: int
    class_name: Optional[str] = None
    tracking_id: Optional[int] = None

    class Config:
        from_attributes = True


class ExpectedResultResponse(BaseModel):
    """DTO für ein Detection Result mit allen zugehörigen Boxes"""
    id: int
    source: Optional[str] = None
    model_name: Optional[str] = None
    created_at: Optional[datetime] = None
    boxes: List[DetectedBoxResponse] = []

    class Config:
        from_attributes = True


class DetectionSummary(BaseModel):
    """DTO für eine Zusammenfassung aller Detektionen"""
    total_results: int
    total_detections: int
    average_confidence: float
    unique_classes: List[str]

