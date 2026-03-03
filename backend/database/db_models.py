from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, JSON, Index
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime, timezone
from dataclasses import dataclass, field
from typing import Optional, Dict, List, Any

Base = declarative_base()


# ===== Typing Models (Dataclasses - nicht in der Datenbank) =====
@dataclass
class KeypointModel:
    """Typisierungsmodell für Keypoint-Daten"""
    data: Optional[Dict[str, Any]] = None  # Koordinaten und Confidence


@dataclass
class MaskModel:
    """Typisierungsmodell für Segmentierungsdaten"""
    data: Optional[Dict[str, Any]] = None  # Segmentierungsdaten


@dataclass
class OBBModel:
    """Typisierungsmodell für Oriented Bounding Box"""
    xyxy: Optional[List[float]] = None
    conf: Optional[List[float]] = None


@dataclass
class OrigImgModel:
    """Typisierungsmodell für Originalbild-Daten"""
    img_data: Optional[Dict[str, Any]] = None


@dataclass
class ProbsModel:
    """Typisierungsmodell für Klassifikations-Wahrscheinlichkeiten"""
    top5: Optional[List[str]] = None
    top5_conf: Optional[List[float]] = None


@dataclass
class PlotModel:
    """Typisierungsmodell für Plot-Daten"""
    path: Optional[str] = None
    save_dir: Optional[str] = None
    names: Optional[Dict[int, str]] = None  # Dict of class names
    orig_shape: Optional[tuple] = None  # [height, width]
    speed: Optional[Dict[str, float]] = None  # Dict mit timing info
    keypoints: Optional[List[KeypointModel]] = field(default_factory=list)
    masks: Optional[List[MaskModel]] = field(default_factory=list)
    obb: Optional[List[OBBModel]] = field(default_factory=list)
    orig_img: Optional[OrigImgModel] = None
    probs: Optional[ProbsModel] = None


# ===== Database Models (ORM Models) =====
class ExpectedResult(Base):
    __tablename__ = "expected_results"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    # Meta
    source = Column(String, nullable=True)  # z.B. Dateiname / Stream-URL
    model_name = Column(String, nullable=True)  # z.B. "yolov8n"

    # Relationship zu den einzelnen Boxen
    boxes = relationship("BoxModel", back_populates="result", cascade="all, delete-orphan")

    __table_args__ = (
        Index('idx_created_at', 'created_at'),
        Index('idx_source', 'source'),
    )


class BoxModel(Base):
    __tablename__ = "detected_boxes"

    id = Column(Integer, primary_key=True, index=True)
    result_id = Column(Integer, ForeignKey("expected_results.id"), nullable=False)

    # Detection Info
    class_id = Column(Integer, nullable=False)
    class_name = Column(String, nullable=True)
    confidence = Column(Float, nullable=False)
    tracking_id = Column(Integer, nullable=True)
    box_metadata = Column(JSON, nullable=True)

    # Koordinaten
    x1 = Column(Float, nullable=False)
    y1 = Column(Float, nullable=False)
    x2 = Column(Float, nullable=False)
    y2 = Column(Float, nullable=False)

    # Relationship
    result = relationship("ExpectedResult", back_populates="boxes")

    __table_args__ = (
        Index('idx_result_id', 'result_id'),
        Index('idx_class_id', 'class_id'),
    )




