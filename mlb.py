from google import genai
from google.genai import types
import base64
import json

class MLBStata:
    def __init__(self, video, text):
        self.video = video
        self.text = text

    def generate(self):
        print(self.text)
        client = genai.Client(
            vertexai=True,
            project="gen-lang-client-0007077132",
            location="us-central1"
        )
        video1 = types.Part.from_uri(
            file_uri=self.video,
            mime_type="video/*",
        )
        text1 = types.Part.from_text("""Examine the video to find occurrences of these metrics:
    Hit Distance
    Exit Velocity
    Launch Angle
    For each occurrence, reference the product in the frame and explain your findings.
    Output Specification
    exmaple:-
    {
    "metrics": [
        {
        "metrics": {
            "Exit Velocity": 101,
            "Hit Distance": 409,
            "Launch Angle": 33
        },
        "timestamp": "00:20"
        }
    ]
    }
    Ensure timestamps are in mm:ss format.""")

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
            temperature=2,
            top_p=0.95,
            max_output_tokens=8192,
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
                                        }
                                    },
                                    "required": ["Exit Velocity", "Launch Angle", "Hit Distance"]
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