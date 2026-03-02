from fastapi import APIRouter, HTTPException
from sqlalchemy.future import select
from database.dbcontext import AsyncSessionLocal
from database.models import DetectionResult
from pydantic import BaseModel
from typing import List, Any, Optional
import logging

router = APIRouter()


class DetectionResultResponse(BaseModel):
    id: int
    boxes: Optional[List[Any]] = None
    masks: Optional[List[Any]] = None
    keypoints: Optional[List[Any]] = None
    probs: Optional[List[Any]] = None
    obb: Optional[List[Any]] = None

    # Dadurch wird das SQLAlchemy-Objekt automatisch ins API-Model gemappt.
    class Config:
        orm_mode = True


@router.get("/result/{id}", response_model=DetectionResultResponse)
async def get_detections(id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(DetectionResult).where(DetectionResult.id == id)
        )
        detection = result.scalar_one_or_none()
        if detection is None:
            raise HTTPException(status_code=404, detail="Result not found")
        logging.info(f"Successfully retrieved detection result with ID {detection}.")
        return detection


@router.get("/results", response_model=List[DetectionResultResponse])
async def get_all_detections():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(DetectionResult))
        detections = result.scalars().all()
        logging.info(f"Successfully retrieved all detection results.")
        return detections
