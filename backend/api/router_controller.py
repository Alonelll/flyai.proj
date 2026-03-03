from fastapi import APIRouter, HTTPException, Query
from backend.database.db_models import BoxModel
from backend.api.api_dto_schemas import ExpectedResultResponse, DetectionSummary
from backend.api.detection_handler_service import DetectionResultService
from typing import List, Optional
import logging

router = APIRouter(prefix="/api", tags=["Detection Results"])

# ===== Single Detection Result Endpoints =====
@router.get("/result/{result_id}", response_model=ExpectedResultResponse)
async def get_detection(result_id: int):
    """Fetch eine einzelne Detection Result mit allen Boxes"""
    detection = await DetectionResultService.get_result_by_id(result_id)

    if detection is None:
        raise HTTPException(status_code=404, detail=f"Detection result {result_id} not found")

    logging.info(f"Detection result {result_id} abgerufen.")
    return detection


# ===== Multiple Detection Results Endpoints =====
@router.get("/results", response_model=List[ExpectedResultResponse])
async def get_all_detections(
    skip: int = Query(0, ge=0, description="Anzahl überspringender Einträge"),
    limit: int = Query(10, ge=1, le=100, description="Maximale Anzahl Ergebnisse"),
    source: Optional[str] = Query(None, description="Filter nach Source"),
    model_name: Optional[str] = Query(None, description="Filter nach Model Name"),
):
    """Fetch alle Detection Results mit Pagination und optionalen Filtern"""
    detections = await DetectionResultService.get_all_results(
        skip=skip, limit=limit, source=source, model_name=model_name
    )
    logging.info(f"{len(detections)} Detection results abgerufen.")
    return detections


@router.get("/results/by-class/{class_id}", response_model=List[ExpectedResultResponse])
async def get_detections_by_class(
    class_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
):
    """Fetch alle Detection Results mit einer bestimmten Klasse"""
    detections = await DetectionResultService.get_results_by_class(
        class_id=class_id, skip=skip, limit=limit
    )
    logging.info(f"Detection results mit class_id {class_id} abgerufen.")
    return detections


@router.get("/results/high-confidence", response_model=List[ExpectedResultResponse])
async def get_high_confidence_detections(
    min_confidence: float = Query(0.8, ge=0.0, le=1.0, description="Minimales Confidence Level"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
):
    """Fetch Detection Results mit hohem Confidence Level"""
    detections = await DetectionResultService.get_high_confidence_results(
        min_confidence=min_confidence, skip=skip, limit=limit
    )
    logging.info(f"High confidence detection results abgerufen (min: {min_confidence}).")
    return detections


# ===== Summary & Analytics Endpoints =====
@router.get("/summary", response_model=DetectionSummary)
async def get_detection_summary():
    """Fetch zusammenfasste Statistiken aller Detektionen"""
    total_results = await DetectionResultService.get_total_count()
    avg_confidence = await DetectionResultService.get_average_confidence()
    unique_classes = await DetectionResultService.get_unique_classes()

    # Berechne total detections (Anzahl der Boxes)
    from backend.database.dbcontext import AsyncSessionLocal
    from sqlalchemy import func
    from sqlalchemy.future import select
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(func.count(BoxModel.id)))
        total_boxes = result.scalar() or 0

    return DetectionSummary(
        total_results=total_results,
        total_detections=total_boxes,
        average_confidence=round(avg_confidence, 2),
        unique_classes=unique_classes
    )


