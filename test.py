from mlb_beck import VideoProcessor
video_url = "https://www.youtube.com/watch?v=fyR9FZMN5C8"
video_processor = VideoProcessor(video_url)
data_json = video_processor.fetch_stats()
pitch = video_processor.generate_insights(data_json)
print(pitch)
# speech_synthesizer = SpeechSynthesizer()
# audio_generator = AudioGenerator(speech_synthesizer, pitch)
# audio_generator.generate_audio_for_insights()