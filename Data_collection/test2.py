from google import genai
from google.genai import types
import base64

def generate():
  client = genai.Client(
      vertexai=True,
      project="gen-lang-client-0007077132",
      location="us-central1"
  )

  video1 = types.Part.from_uri(
      file_uri="https://youtu.be/fyR9FZMN5C8?si=FioUIUndO4u-Q6GF",
      mime_type="video/*",
  )
  prompt_text = """Examine the video to find occurrences of these metrics:
    Pitch Speed
    Exit Velocity
    Spin Rate
    Launch Angle
    Barrel Rate
    Sprint Speed
    Catch Probability
    For each occurrence, reference the product in the frame and explain your findings.
    Output Specification
    Ensure timestamps are in mm:ss format. If no metrics are found, output nothing. Avoid hallucinating results."""

  text1 = types.Part(text=prompt_text)

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
  generate_content_config = types.GenerateContentConfig(
    temperature = 2,
    top_p = 0.95,
    max_output_tokens = 8192,
    response_modalities = ["TEXT"],
    safety_settings = [types.SafetySetting(
      category="HARM_CATEGORY_HATE_SPEECH",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_DANGEROUS_CONTENT",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_HARASSMENT",
      threshold="OFF"
    )],
  )

  for chunk in client.models.generate_content_stream(
    model = model,
    contents = contents,
    config = generate_content_config,
    ):
    print(chunk, end="")

generate()