from pydantic import BaseModel
from datetime import datetime
from fastapi import UploadFile, File

class AudioBase(BaseModel):
    id: int
    audio: UploadFile
    user_text: str
    blessi_text: str
    timestamp: datetime

class AudioDisplay(BaseModel):
    audio: UploadFile = File(...)