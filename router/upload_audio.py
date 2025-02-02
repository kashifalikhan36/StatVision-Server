from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import FileResponse,JSONResponse
from sqlalchemy.orm import Session
from database.database import get_db
from database.db_audio import create
import json
# import gtts as gTTS
import os
from mlb_beck import VideoProcessor, SpeechSynthesizer, AudioGenerator
from video_processing import StatcastImageCreator, VideoOverlay

router = APIRouter(
    prefix="/audio",
    tags=["Audio"]
)

# @router.get("/audio_output")
# async def upload_audio(db: Session = Depends(get_db)):
#     return FileResponse("audios/output.wav", media_type="audio/mpeg")



@router.get("/generate-video/")
async def mlb_video_generator():
    # video_url = text
    # video_processor = VideoProcessor(video_url)
    # data_json = video_processor.fetch_stats()
    # pitch = video_processor.generate_insights(data_json)

    # speech_synthesizer = SpeechSynthesizer()
    # audio_generator = AudioGenerator(speech_synthesizer, pitch)
    # audio_generator.generate_audio_for_insights()

    temp_audio_path = os.path.join("audio_output", "commentary_00-04_0.wav")
    statcast_creator = StatcastImageCreator(json_path="temp/statcast_data.json", 
                                       font_bold_path="./fonts/DejaVuSans-Bold.ttf", 
                                       font_regular_path="./fonts/DejaVuSans.ttf")
    statcast_creator.generate_stat_images()

    video_overlay = VideoOverlay(video_path="./temp/video_temp.mp4", 
                                audio_path="./audio_output/commentary.wav", 
                                images_dir="./temp/images")
    video_overlay.create_image_clips()
    video_overlay.overlay_images_on_video()
    video_path = "./temp/output_video.mp4"  # Replace with your video file path
    print("Video resoponse")
    return FileResponse(video_path, media_type="video/mp4", filename="mlb_insights.mp4")


@router.post("/url-to-speech/")
async def url_to_speech(text: str):
    video_url = text
    video_processor = VideoProcessor(video_url)
    data_json = video_processor.fetch_stats()
    pitch = video_processor.generate_insights(data_json)

    speech_synthesizer = SpeechSynthesizer()
    audio_generator = AudioGenerator(speech_synthesizer, pitch)
    audio_generator.generate_audio_for_insights()
    file_path = "./temp/statcast_data.json"
    
    # Open and read the JSON file
    with open(file_path, "r") as file:
        data = json.load(file)
    print("Stats resoponse")
    # Return the data as a JSON response
    return JSONResponse(content=data)
