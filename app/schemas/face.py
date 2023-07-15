from pydantic import BaseModel

class FaceData(BaseModel):
    device_id:str
    face_id:str
