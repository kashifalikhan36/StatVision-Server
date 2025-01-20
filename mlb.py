from google import genai
from google.genai import types
import base64
import json

class MLBStata:
    def __init__(self, video):
        self.video = video
        # self.text = text
        
    def generate_insights(self,exit_velocity, hit_distance, launch_angle, spray_angle, pitch_type, performance_score, ball_trajectory, predicted_outcome, home_run_fav,):
        # Initialize the client
        client = genai.Client(
            vertexai=True,
            project="gen-lang-client-0007077132",
            location="us-central1"
        )

        # Define video and text input
        video1 = types.Part.from_uri(
            file_uri=self.video,
            mime_type="video/*",
        )

        text1 = types.Part.from_text(f"""
            You will receive a set of MLB match statistics including:

            - Exit Velocity: {exit_velocity}
            - Hit Distance: {hit_distance}
            - Launch Angle: {launch_angle}
            - Spray Angle: {spray_angle}
            - Pitch Type: {pitch_type}
            - Performance Score: {performance_score}
            - Ball Trajectory: {ball_trajectory}
            - Predicted Outcome: {predicted_outcome}
            - Home Run Favorability: {home_run_fav}"""+"""
            Your task is to generate engaging, live-style commentary based on these metrics. Each commentary should correspond to a video timestamp, and if a player is identifiable, include their name. The pitch should feel real and dynamic, matching the tone of a live MLB broadcast.  

            **Output Format:**  
            A JSON object with an array of insights, each containing:
            1. `timestamp`: the moment in the video.
            2. `commentary`: a fun and insightful narration of the play, referencing the metrics.

            Example output:  
            '''
            {
                "insights": [
                    {
                        "timestamp": "{timestamp}",
                        "commentary": f"With an exit velocity of {Exit_velocity} mph and a launch angle of {Launch_angle} degrees, the ball takes off with a {Ball_trajectory} trajectory, traveling {Hit_distance} feet. It looks like a {Predicted_outcome}, and with a home run favorability of {Home_run_favorability}%, this could be one for the history books!"
                    },
                    {
                        "timestamp": "{timestamp}",
                        "commentary": f"A {Pitch_type} pitch at {Performance_score} performance score meets the bat at a {Spray_angle}-degree spray angle, sending it flying to {Hit_distance} feet. What a hit!"
                    }
                ]
            }
            '''json
        """)

        # Define the model and contents
        model = "gemini-2.0-flash-exp"
        contents = [
            types.Content(
                role="user",
                parts=[
                    video1,
                    text1
                ]
            )
        ]

        # Configure the content generation parameters
        generate_content_config = types.GenerateContentConfig(
            temperature=0.7,
            top_p=0.9,
            max_output_tokens=2048,
            response_modalities=["TEXT"],
            safety_settings=[
                types.SafetySetting(
                    category="HARM_CATEGORY_HATE_SPEECH",
                    threshold="OFF"
                ),
                types.SafetySetting(
                    category="HARM_CATEGORY_DANGEROUS_CONTENT",
                    threshold="OFF"
                ),
                types.SafetySetting(
                    category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    threshold="OFF"
                ),
                types.SafetySetting(
                    category="HARM_CATEGORY_HARASSMENT",
                    threshold="OFF"
                )
            ],
            response_mime_type="application/json",
            response_schema={
                "type": "OBJECT",
                "properties": {
                    "insights": {
                        "type": "ARRAY",
                        "items": {
                            "type": "OBJECT",
                            "properties": {
                                "timestamp": {
                                    "type": "STRING",
                                    "description": "Time of the event in mm:ss format"
                                },
                                "commentary": {
                                    "type": "STRING",
                                    "description": "Fun and engaging commentary for the metrics"
                                }
                            },
                            "required": ["timestamp", "commentary"]
                        }
                    }
                }
            }
        )

        # Generate content stream using the configured model and parameters
        j = ""
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            j += chunk.text

        return json.loads(j)
    
    def generate_stats(self):
        # print(self.text)
        client = genai.Client(
            vertexai=True,
            project="gen-lang-client-0007077132",
            location="us-central1"
        )
        video1 = types.Part.from_uri(
            file_uri=self.video,
            mime_type="video/*",
        )
        text1 = types.Part.from_text("""
            Examine the video to find occurrences of these metrics: 
            - Exit Velocity  
            - Hit Distance  
            - Launch Angle  
            - Spray Angle  
            - Pitch Type  

            For each occurrence, reference the product in the frame and explain your findings.

            **Output Specification:**  
            Example:
            ```json
            {
                "metrics": [
                    {
                        "metrics": {
                            "Exit Velocity": 101,
                            "Hit Distance": 409,
                            "Launch Angle": 33,
                            "Spray Angle": 25,
                            "Pitch Type": "Fastball"
                        },
                        "timestamp": "00:20"
                    }
                ]
            }
            ```
            Ensure timestamps are in **mm:ss** format.

            """)

        # Define the model and contents
        model = "gemini-2.0-flash-exp"
        contents = [
            types.Content(
                role="user",
                parts=[
                    video1,
                    text1
                ]
            )
        ]

        # Configure the content generation parameters
        generate_content_config = types.GenerateContentConfig(
            temperature=0.7,
            top_p=0.9,
            max_output_tokens=4096,
            response_modalities=["TEXT"],
            safety_settings=[
                types.SafetySetting(
                    category="HARM_CATEGORY_HATE_SPEECH",
                    threshold="OFF"
                ),
                types.SafetySetting(
                    category="HARM_CATEGORY_DANGEROUS_CONTENT",
                    threshold="OFF"
                ),
                types.SafetySetting(
                    category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    threshold="OFF"
                ),
                types.SafetySetting(
                    category="HARM_CATEGORY_HARASSMENT",
                    threshold="OFF"
                )
            ],
            response_mime_type="application/json",
            response_schema = {
                "type": "OBJECT",
                "properties": {
                    "metrics": {
                        "type": "ARRAY",
                        "items": {
                            "type": "OBJECT",
                            "properties": {
                                "timestamp": {
                                    "type": "STRING",
                                    "description": "Time of the event in mm:ss format"
                                },
                                "metrics": {
                                    "type": "OBJECT",
                                    "properties": {
                                        "Exit Velocity": {
                                            "type": "INTEGER",
                                            "description": "Speed of the ball after contact"
                                        },
                                        "Launch Angle": {
                                            "type": "INTEGER",
                                            "description": "The angle at which the ball is hit or thrown"
                                        },
                                        "Hit Distance": {
                                            "type": "INTEGER",
                                            "description": "The distance the ball travels after being hit"
                                        },
                                        "Spray Angle": {
                                            "type": "NUMBER",
                                            "description": "Direction of the hit relative to the field (pull, center, opposite field)"
                                        },
                                        "Pitch Type": {
                                            "type": "STRING",
                                            "description": "Classification of the pitch (e.g., fastball, curveball)"
                                        }
                                    },
                                    "required": [
                                        "Exit Velocity", 
                                        "Launch Angle", 
                                        "Hit Distance", 
                                        "Spray Angle", 
                                        "Pitch Type"
                                    ]
                                }
                            },
                            "required": ["timestamp", "metrics"]
                        }
                    }
                }
            }

        )
        i=0
        j=""
        # Generate content stream using the configured model and parameters
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            j+=chunk.text
        return json.loads(j)