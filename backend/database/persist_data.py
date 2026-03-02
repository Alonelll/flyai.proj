import logging
from database.dbcontext import AsyncSessionLocal
from database.models import DetectionResult


# 1) eine Session erstellen, die ich später verwenden kann, um Daten in die Datenbank zu schreiben
# 2) die Daten die ich speichern möchte nehme ich aus meiner service file entgegen


async def add_results(result):
    async with AsyncSessionLocal() as session:
        result_dict = DetectionResult(
            boxes=[box.to_dict() for box in result.boxes] if result.boxes else [],
            masks=[mask.to_dict() for mask in result.masks] if result.masks else [],
            keypoints=[kp.to_dict() for kp in result.keypoints]
            if result.keypoints
            else [],
            probs=result.probs,
            obb=[o.to_dict() for o in result.obb] if result.obb else [],
        )
        try:
            print(result)
            session.add(result_dict)
            await session.flush()
        except Exception as e:
            logging.error(
                f"Hier scheitert Json aus der Methode wo ich Daten in die Database schreiben möchte Fehler: {e}"
            )
        await session.commit()
