import os
import numpy as np
from PIL import Image, ImageDraw
from moviepy import VideoFileClip, ImageClip, CompositeVideoClip, AudioFileClip

# Paths
video_path = "./temp/video_temp.mp4"
audio_path = "./audio_output/commentary.wav"
images_dir = "./temp/images"
output_path = "./temp/output_video.mp4"

# Load the video
video = VideoFileClip(video_path)

# Load all images from the directory
image_files = [os.path.join(images_dir, img) for img in os.listdir(images_dir) if img.endswith(('.png', '.jpg', '.jpeg'))]
images = [ImageClip(img).with_duration(video.duration / len(image_files)) for img in image_files]

# Function to add rounded corners to an image
def add_rounded_corners(image_clip, radius=20):
    # Convert the image clip to a PIL image
    frame = image_clip.get_frame(0)  # Get the first frame
    pil_image = Image.fromarray(frame)  # Convert NumPy array to PIL image

    # Create a mask with rounded corners
    mask = Image.new("L", pil_image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), pil_image.size], radius=radius, fill=255)

    # Apply the mask to the image
    pil_image.putalpha(mask)
    return ImageClip(np.array(pil_image))

# Resize, position, and add rounded corners to images
for i, img in enumerate(images):
    img = img.resized(height=250)  # Resize image to fit the corner
    img = add_rounded_corners(img, radius=20)  # Add rounded corners
    img = img.with_position(("left", "bottom"))  # Position at bottom-left corner
    # img = img.crossfadein(1).crossfadeout(1)  # Add fade-in and fade-out
    images[i] = img

# Create a list of clips with each image appearing one after another
image_clips = []
for i, img in enumerate(images):
    start_time = i * (video.duration / len(images))
    end_time = (i + 1) * (video.duration / len(images))
    img = img.with_start(start_time).with_end(end_time)
    image_clips.append(img)

# Overlay images on the video
final_video = CompositeVideoClip([video] + image_clips)

# Add audio to the final video
audio = AudioFileClip(audio_path)
final_video = final_video.with_audio(audio)

# Export the final video
final_video.write_videofile(output_path, codec="libx264", fps=24)

print(f"Video saved to {output_path}")
