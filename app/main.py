from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session
import databaseutils
from schemas.face import FaceData
from models.face import FaceCapture
from datetime import datetime

app=FastAPI()

@app.get("/", tags=["Default"])
def read_root():
    return {"Hello": "World"}

@app.post("/face-data")
def captureFace(FaceData:FaceData,db: Session = Depends(databaseutils.get_db)):
    
    try:
        face=FaceCapture(
            device_id=FaceData.device_id,
            face_id =FaceData.face_id,
            date=datetime.now()
        )
        db.add(face)
        db.commit()
        
    except:
        raise HTTPException(500,"Something Went Wrong")

    return "Data Added Succesfully"