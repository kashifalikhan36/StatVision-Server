from mlb import MLBStata
import time
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import joblib
from google.cloud import texttospeech

# Video input and MLBStata processing
video = "https://sporty-clips.mlb.com/OTlCWmdfWGw0TUFRPT1fRDFKWlZGRUFVMUVBRHdRQkJBQUFBdzlSQUZsUlUxUUFCVkpYQXdjQkJncFVCbFFI.mp4"
print("Jay Bruce homers")
mlbstuff = MLBStata(video)

try:
    data_json = mlbstuff.generate_stats()
except:
    time.sleep(120)
    data_json = mlbstuff.generate_stats()

# Print data for verification
for metric in data_json["metrics"]:
    print(f"Timestamp: {metric['timestamp']}")
    for key, value in metric["metrics"].items():
        print(f"  {key}: {value}")
print(data_json)

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

# Display Results
print(df.head())
print(df.columns)
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

pitch=mlbstuff.generate_insights(exit_velocity, hit_distance, launch_angle, spray_angle, pitch_type, performance_score, ball_trajectory, predicted_outcome, home_run_fav)
print(pitch)


def synthesize_speech(text, output_file="output.mp3"):
    """
    Synthesizes speech from the input text and saves it to an audio file.

    Args:
    text (str): The input text to be synthesized into speech.
    output_file (str): The name of the output audio file (default is 'output.mp3').

    Returns:
    None
    """
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Build the voice request, select the language code ("en-US") and the voice name ("en-US-Casual-K")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Casual-K"  # The specific voice name you requested
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(output_file, "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_file}"')

def extract_enerate_audio_for_insights(insights):
    
    for id,i in enumerate(pitch["insights"]):
        commentary = i['commentary']
        timestamp = i['timestamp']

        # Create a filename based on the timestamp
        output_filename = f"audio_output\commentary_{timestamp.replace(':', '-')}_{id}.wav"
        
        # Synthesize speech for the commentary
        synthesize_speech(commentary, output_filename)
extract_enerate_audio_for_insights(pitch)
# synthesize_speech(extract_enerate_audio_for_insights(pitch),"audio_output/audio.mp3")