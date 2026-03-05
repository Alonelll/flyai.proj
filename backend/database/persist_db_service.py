import logging
from backend.database.dbcontext import AsyncSessionLocal
from backend.database.db_models import ExpectedResult, BoxModel


async def add_results(result):
    # Früh raus wenn es keine Boxen gibt - nicht speichern!
    if result.boxes is None or len(result.boxes) == 0:
        logging.debug("Keine Detektionen gefunden - übersprungen.")
        return None

    async with AsyncSessionLocal() as session:
        # 1) ExpectedResult anlegen
        detection_result = ExpectedResult(
            source=getattr(result, "path", None),
            model_name=getattr(result, "model_name", None),  # steht aktuell nix drinne
        )
        session.add(detection_result)
        await session.flush()  # ID generieren lassen

        # 2) Boxes mappen
        boxes = result.boxes
        names = result.names

        for i in range(len(boxes)):
            x1, y1, x2, y2 = boxes.xyxy[i].tolist()
            cls_id = int(boxes.cls[i])

            box = BoxModel(
                result_id=detection_result.id,
                x1=x1,
                y1=y1,
                x2=x2,
                y2=y2,
                confidence=float(boxes.conf[i]),
                class_id=cls_id,
                class_name=names.get(cls_id),
                tracking_id=int(boxes.id[i])
                if boxes.is_track
                else None,  # Wenn Object getrackt wurde setze hier Id des Trackings, sonst None
            )
            print(f"Hier Box Infos: {box}")
            session.add(box)

        try:
            await session.commit()
            logging.info(f"Detection result {detection_result.id} gespeichert.")
            return detection_result.id
        except Exception as e:
            await session.rollback()
            logging.error(f"Fehler beim Speichern: {e}")
            raise
