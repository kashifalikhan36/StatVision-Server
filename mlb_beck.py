from mlb import MLBStata
import time
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import joblib
from google.cloud import texttospeech
import json
import os

class VideoProcessor:
    def __init__(self, video_url):
        self.video_url = video_url
        self.mlbstuff = MLBStata(video_url)

    def fetch_stats(self):
        try:
            data_json = self.mlbstuff.generate_stats()
        except:
            time.sleep(120)
            data_json = self.mlbstuff.generate_stats()
        return data_json

    def generate_insights(self, data_json):
        # Input Data
        data = data_json

        # Label Encoder for Pitch Type
        pitch_types = ['Fastball', 'Curveball', 'Slider', 'Changeup']  # Example pitch types
        label_encoder = LabelEncoder()
        label_encoder.fit(pitch_types)

        # Load Models
        model_outcome = joblib.load('models/random_forest_classifier_outcome_fold0.joblib')
        model_home_run_favorability = joblib.load('models/random_forest_regressor_home_run_favorability_fold2.joblib')

        # Function Definitions
        def calculate_performance_score(row):
            return (row['Exit Velocity'] * 0.3) + (row['Hit Distance'] * 0.3) + (row['Launch Angle'] * 0.2) + (row['Spray Angle'] * 0.1) + (row['Pitch Type'] * 0.1)

        def calculate_ball_trajectory(row):
            return row['Launch Angle'] * row['Exit Velocity']

        metrics_data = [entry['metrics'] for entry in data['metrics']]
        df = pd.DataFrame(metrics_data)

        df['Pitch Type'] = label_encoder.transform(df['Pitch Type'])

        df['Performance Score'] = df.apply(calculate_performance_score, axis=1)
        df['Ball Trajectory'] = df.apply(calculate_ball_trajectory, axis=1)

        X_classification = df[['Exit Velocity', 'Hit Distance', 'Launch Angle', 'Spray Angle', 'Pitch Type', 'Performance Score', 'Ball Trajectory']]
        X_regression = X_classification

        df['Predicted Outcome'] = model_outcome.predict(X_classification)
        df['Home Run Favorability'] = model_home_run_favorability.predict(X_regression)

        row = df.iloc[0]

        # Extract values as integers for the function call
        exit_velocity = int(row['Exit Velocity'])
        hit_distance = int(row['Hit Distance'])
        launch_angle = int(row['Launch Angle'])
        spray_angle = int(row['Spray Angle'])
        pitch_type = row['Pitch Type']
        performance_score = int(row['Performance Score'])
        ball_trajectory = row['Ball Trajectory']
        predicted_outcome = row['Predicted Outcome']
        home_run_fav = int(row['Home Run Favorability'])

        player_name = data['metrics'][0].get('player', 'Unknown Player')

        statcast_dict = {
            "Exit Velocity": exit_velocity,
            "Hit Distance": hit_distance,
            "Launch Angle": launch_angle,
            "Spray Angle": spray_angle,
            "Pitch Type": pitch_type,
            "Performance Score": performance_score,
            "Ball Trajectory": ball_trajectory,
            "Predicted Outcome": predicted_outcome,
            "Home Run Favorite": home_run_fav,
            "Player": player_name
        }
        os.makedirs("temp", exist_ok=True)
        json_path = os.path.join("temp", "statcast_data.json")
        with open(json_path, "w") as json_file:
            json.dump(statcast_dict, json_file, indent=4)

        pitch = self.mlbstuff.generate_insights(exit_velocity, hit_distance, launch_angle, spray_angle, pitch_type, performance_score, ball_trajectory, predicted_outcome, home_run_fav)

        return pitch


class SpeechSynthesizer:
    def __init__(self, language_code="en-US", voice_name="en-US-Casual-K"):
        self.language_code = language_code
        self.voice_name = voice_name

    def synthesize_speech(self, text, output_file="output.mp3"):
        """
        Synthesizes speech from the input text and saves it to an audio file.
        """
        # Instantiates a client
        client = texttospeech.TextToSpeechClient()

        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=text)

        # Build the voice request, select the language code and voice name
        voice = texttospeech.VoiceSelectionParams(
            language_code=self.language_code,
            name=self.voice_name
        )

        # Select the type of audio file you want returned
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        # Perform the text-to-speech request
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # Save the audio content
        with open(output_file, "wb") as out:
            out.write(response.audio_content)
            print(f'Audio content written to file "{output_file}"')


class AudioGenerator:
    def __init__(self, synthesizer, insights_data):
        self.synthesizer = synthesizer
        self.insights_data = insights_data

    def generate_audio_for_insights(self):
        text=""
        for id, insight in enumerate(self.insights_data["insights"]):
            commentary = insight['commentary']
            text+=" "+commentary
            # Create a filename based on the timestamp
        output_filename = f"audio_output\commentary.wav"
        self.synthesizer.synthesize_speech(commentary, output_filename)