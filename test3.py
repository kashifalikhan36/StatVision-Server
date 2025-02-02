import os
import numpy as np
from PIL import Image, ImageDraw
from moviepy import VideoFileClip, ImageClip, CompositeVideoClip, AudioFileClip, AudioArrayClip, concatenate_audioclips 

# Paths
video_path = "./temp/video_temp.mp4"
audio_path = "./audio_output/commentary.wav"
folder_path = './temp'

# List of supported image extensions
image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']

# Collect all image files from the folder
image_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if any(f.lower().endswith(ext) for ext in image_extensions)]

# Load video without audio
video = VideoFileClip(video_path).without_audio()
video_w, video_h = video.size

# Load new audio file
audio = AudioFileClip(audio_path)

# If audio is shorter than the video, extend it with silence
if audio.duration < video.duration:
    silence_duration = video.duration - audio.duration
    silence = AudioArrayClip(np.zeros((int(silence_duration * audio.fps), 2)), fps=audio.fps)
    audio = concatenate_audioclips([audio, silence])

# Ensure audio duration matches video
# Ensure audio duration matches video
audio = audio.with_duration(video.duration)

# Function to resize and apply rounded edges to images
def process_image(image_path, size=(300, 150), corner_radius=30):
    img = Image.open(image_path).convert("RGBA")
    img = img.resize(size, Image.LANCZOS)

    # Create a rounded mask
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, size[0], size[1]), radius=corner_radius, fill=255)

    # Apply rounded mask
    img.putalpha(mask)

    # Save temporary processed image
    temp_path = f"temp_processed_{os.path.basename(image_path)}"
    img.save(temp_path)

    return temp_path

# Generate image clips with animation
image_clips = []
num_images = len(image_paths)
total_duration = video.duration
interval = total_duration / (num_images + 1)  # Space out images

for i, image_path in enumerate(image_paths):
    processed_img_path = process_image(image_path)

    # Create an ImageClip
    img_clip = (ImageClip(processed_img_path, duration=3)  # Display for 3 seconds
                .set_position(("left", "bottom"))  # Bottom-left corner
                .fadein(0.5)  # Fade-in animation
                .fadeout(0.5)  # Fade-out animation
                .set_start(interval * (i + 1)))  # Appear at different times

    image_clips.append(img_clip)

# Combine video with overlay images
final_clip = CompositeVideoClip([video] + image_clips)

# Add fixed audio to the final video
final_clip = final_clip.with_audio(audio)

# Output final video
output_path = "output_video.mp4"
final_clip.write_videofile(output_path, codec="libx264", fps=video.fps, audio_codec="aac")

# Cleanup temporary images
for img in image_paths:
    temp_img = f"temp_processed_{os.path.basename(img)}"
    if os.path.exists(temp_img):
        os.remove(temp_img)

print("✅ Video processing complete! Check 'output_video.mp4'")
