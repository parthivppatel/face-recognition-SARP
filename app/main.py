from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .databaseutils import get_db
from .schemas.face import FaceData, FaceID
from .models.face import FaceCapture
from datetime import datetime

app = FastAPI()


@app.get("/", tags=["Default"])
def read_root():
    return {"Hello": "World"}


@app.post("/face-data")
def captureFace(FaceData: FaceData, db: Session = Depends(get_db)):
    try:
        face = FaceCapture(
            device_id=FaceData.device_id, face_id=FaceData.face_id, date=datetime.now()
        )
        db.add(face)
        db.commit()

    except:
        raise HTTPException(500, "Something Went Wrong")

    return {"Response": "Data Added Succesfully"}


@app.post("/get-time-stamp")
def captureFace(FaceID: FaceID, db: Session = Depends(get_db)):
    try:
        print(FaceID.face_id)
        time_stamp = (
            db.query(FaceCapture.date)
            .filter(FaceCapture.face_id == FaceID.face_id)
            .order_by(FaceCapture.date.desc())
        )

    except:
        raise HTTPException(500, "Something Went Wrong")

    return time_stamp
