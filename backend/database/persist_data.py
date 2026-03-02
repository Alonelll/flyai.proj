import logging
from database.dbcontext import AsyncSessionLocal
from database.models import DetectionResult
import json


# 1) eine Session erstellen, die ich später verwenden kann, um Daten in die Datenbank zu schreiben oder zu lesen
# 2) die Daten die ich speichern möchte nehme ich aus meiner service file entgegen


async def add_results(result):
    async with AsyncSessionLocal() as session:
        result_dict = DetectionResult(
            boxes=result.boxes,
            masks=result.masks,
            keypoints=result.keypoints,
            probs=result.probs,
            obb=result.obb,
        )
        try:
            print(result)

            session.add(result_dict)
            await session.flush()

            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=4)

            logging.info(
                f"Persisting data for track_id: {result.track_id}, name: {result.name}, confidence: {result.confidence}"
            )
        except Exception as e:
            logging.error(
                f"Hier scheitert Json aus der Methode wo ich Daten in die Database schreiben möchte Fehler: {e}"
            )

        # frame = Frame(
        #     track_id=result.track_id,
        #     timestamp=datetime.datetime.now(datetime.UTC),
        #     # id=uuid.uuid4().int, # erstmal auskommentiert lassen da ich  ich nicht weiß ob die Id beim erstellen der DB generiert wird
        #     # image_path=result.path,
        #     # video_id=result.path,  # Using result.path as a video identifier
        # )
        #
        # session.add(frame)
        # await session.flush()  # frame.id wird erzeugt
        #
        # if result.boxes:
        #     for box in result.boxes:
        #         detected_object = DetectedObject(
        #             frame_id=frame.id,
        #             label=result.name,
        #             confdence=result.confidence,
        #             bbox_x1=box.x1,
        #             bbox_y1=box.y1,
        #             bbox_x2=box.x2,
        #             bbox_y2=box.y2,
        #             track_id=result.track_id,
        #             # label=str(box.cls.item()),
        #             # confidence=float(box.conf.item()),
        #             # bbox_x=float(box.xyxy[0][0]),
        #             # bbox_y=float(box.xyxy[0][1]),
        #             # bbox_width=float(box.xyxy[0][2]),
        #             # bbox_height=float(box.xyxy[0][3]),
        #             # track_id=int(box.id.item()) if box.id is not None else None,
        #         )
        #
        #         session.add(detected_object)
        #
        await session.commit()
