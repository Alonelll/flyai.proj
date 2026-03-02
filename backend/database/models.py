from sqlalchemy import Column, Integer, JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Info: Hier nur Models die ich in dei Datenbank speichern möchte


class DetectionResult(Base):
    __tablename__ = "detection_results"

    id = Column(Integer, primary_key=True, index=True)
    boxes = Column(JSON, nullable=True)
    masks = Column(JSON, nullable=True)
    keypoints = Column(JSON, nullable=True)
    probs = Column(JSON, nullable=True)
    obb = Column(JSON, nullable=True)
