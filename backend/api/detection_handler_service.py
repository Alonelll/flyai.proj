"""
Business Logic für Detection Results
"""
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import desc, func
from backend.database.dbcontext import AsyncSessionLocal
from backend.database.db_models import ExpectedResult, BoxModel
from typing import List, Optional


class DetectionResultService:
    """Service für alle Detection Result Operationen"""

    @staticmethod
    async def get_result_by_id(result_id: int) -> Optional[ExpectedResult]:
        """Hole ein Detection Result mit allen Boxes"""
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(ExpectedResult)
                .where(ExpectedResult.id == result_id)
                .options(selectinload(ExpectedResult.boxes))
            )
            return result.scalar_one_or_none()

    @staticmethod
    async def get_all_results(
        skip: int = 0,
        limit: int = 100,
        source: Optional[str] = None,
        model_name: Optional[str] = None,
    ) -> List[ExpectedResult]:
        """Hole alle Detection Results mit optionalen Filtern - sortiert nach created_at (neueste zuerst)"""
        async with AsyncSessionLocal() as session:
            query = select(ExpectedResult).options(selectinload(ExpectedResult.boxes))

            if source:
                query = query.where(ExpectedResult.source.ilike(f"%{source}%"))
            if model_name:
                query = query.where(ExpectedResult.model_name == model_name)

            # Sortierung: created_at DESC (neueste zuerst), dann ID DESC als Fallback
            query = query.order_by(desc(ExpectedResult.created_at), desc(ExpectedResult.id)).offset(skip).limit(limit)
            result = await session.execute(query)
            return result.scalars().all()

    @staticmethod
    async def get_results_by_class(
        class_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> List[ExpectedResult]:
        """Hole alle Detection Results mit einer bestimmten Klasse - sortiert nach created_at (neueste zuerst)"""
        async with AsyncSessionLocal() as session:
            query = (
                select(ExpectedResult)
                .options(selectinload(ExpectedResult.boxes))
                .join(BoxModel)
                .where(BoxModel.class_id == class_id)
                .distinct()
                .order_by(desc(ExpectedResult.created_at), desc(ExpectedResult.id))
                .offset(skip)
                .limit(limit)
            )
            result = await session.execute(query)
            return result.scalars().all()

    @staticmethod
    async def get_high_confidence_results(
        min_confidence: float = 0.8,
        skip: int = 0,
        limit: int = 100,
    ) -> List[ExpectedResult]:
        """Hole Detection Results mit hohem Confidence - sortiert nach created_at (neueste zuerst)"""
        async with AsyncSessionLocal() as session:
            query = (
                select(ExpectedResult)
                .options(selectinload(ExpectedResult.boxes))
                .join(BoxModel)
                .where(BoxModel.confidence >= min_confidence)
                .distinct()
                .order_by(desc(ExpectedResult.created_at), desc(ExpectedResult.id))
                .offset(skip)
                .limit(limit)
            )
            result = await session.execute(query)
            return result.scalars().all()

    @staticmethod
    async def get_total_count() -> int:
        """Hole die Gesamtanzahl aller Detection Results"""
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(func.count(ExpectedResult.id)))
            return result.scalar() or 0

    @staticmethod
    async def get_average_confidence() -> float:
        """Hole den Durchschnitt der Confidence-Werte"""
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(func.avg(BoxModel.confidence)))
            return float(result.scalar() or 0.0)

    @staticmethod
    async def get_unique_classes() -> List[str]:
        """Hole alle einzigartigen Klassennamen"""
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(func.array_agg(func.distinct(BoxModel.class_name)))
            )
            classes = result.scalar() or []
            return [c for c in classes if c is not None]

