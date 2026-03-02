from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
import datetime
from sqlalchemy import JSON

Base = declarative_base()

# Hier habe ich meine Models mit die als Typen für die Datenbanktabellen dienen


class Frame(Base):
    __tablename__ = "frames"
    id = Column(Integer, primary_key=True)
    image_path = Column(String, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.datetime.now(datetime.UTC))
    video_id = Column(String, nullable=True)
    objects = relationship("DetectedObject", back_populates="frame")
    track_id = Column(Integer, nullable=True)  # Tracking-ID, optional


class DetectedObject(Base):
    __tablename__ = "detected_objects"
    id = Column(Integer, primary_key=True)
    frame_id = Column(Integer, ForeignKey("frames.id"))
    label = Column(String, nullable=False)
    confidence = Column(Float)
    bbox_x = Column(Float)
    bbox_y = Column(Float)
    bbox_width = Column(Float)
    bbox_height = Column(Float)
    track_id = Column(Integer, nullable=True)  # Tracking-ID, optional
    frame = relationship("Frame", back_populates="objects")


class DetectionResult(Base):
    __tablename__ = "detection_results"

    id = Column(Integer, primary_key=True, index=True)
    boxes = Column(JSON, nullable=True)  # Store bounding box data as JSON
    masks = Column(JSON, nullable=True)  # Store mask data as JSON
    keypoints = Column(JSON, nullable=True)  # Store keypoints as JSON
    probs = Column(JSON, nullable=True)  # Store classification probabilities as JSON
    obb = Column(JSON, nullable=True)  # Store oriented bounding boxes as JSON
