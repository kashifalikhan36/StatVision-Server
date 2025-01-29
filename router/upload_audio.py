from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from database.database import get_db
from database.db_audio import create
# import gtts as gTTS
import os
from mlb_beck import VideoProcessor, SpeechSynthesizer, AudioGenerator

router = APIRouter(
    prefix="/audio",
    tags=["Audio"]
)

@router.get("/audio_output")
async def upload_audio(db: Session = Depends(get_db)):
    return FileResponse("audios/output.wav", media_type="audio/mpeg")

@router.post("/text-to-speech/")
async def text_to_speech(text: str):
    video_url = text
    video_processor = VideoProcessor(video_url)
    data_json = video_processor.fetch_stats()
    pitch = video_processor.generate_insights(data_json)

    speech_synthesizer = SpeechSynthesizer()
    audio_generator = AudioGenerator(speech_synthesizer, pitch)
    audio_generator.generate_audio_for_insights()

    try:
        # Create a temporary file to store the audio
        temp_audio_path = os.path.join("audio_output", "commentary_00-04_0.wav")
        return FileResponse(temp_audio_path, media_type="audio/mpeg", filename="audio_output.wav")
    
    except Exception as e:
        return {"error": f"An error occurred while converting text to speech: {str(e)}"}
