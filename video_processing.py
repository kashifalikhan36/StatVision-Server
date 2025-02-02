import os
import json
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from moviepy import VideoFileClip, ImageClip, CompositeVideoClip, AudioFileClip


class StatcastImageCreator:
    def __init__(self, json_path, font_bold_path, font_regular_path, output_dir="temp/images"):
        self.json_path = json_path
        self.font_bold_path = font_bold_path
        self.font_regular_path = font_regular_path
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.statcast_dict = self._load_statcast_data()

    def _load_statcast_data(self):
        with open(self.json_path, "r") as json_file:
            statcast_dict = json.load(json_file)
        player_name = statcast_dict.get("Player", "Unknown Player")
        del statcast_dict["Player"]
        return player_name, list(statcast_dict.items())

    def create_statcast_template(self, stat1, value1, stat2, value2, player_name, output_path):
        width, height = 550, 520
        background_color = (255, 255, 255)
        img = Image.new("RGB", (width, height), background_color)
        draw = ImageDraw.Draw(img)

        title_font = ImageFont.truetype(self.font_bold_path, 45)
        name_font = ImageFont.truetype(self.font_bold_path, 35)
        stat_font = ImageFont.truetype(self.font_bold_path, 50)
        unit_font = ImageFont.truetype(self.font_regular_path, 30)

        draw.rectangle([(0, 0), (width, 100)], fill=(245, 245, 245))
        draw.text((50, 20), "STATCAST", fill=(0, 0, 0), font=title_font)
        draw.text((50, 70), "Powered by Google Cloud", fill=(50, 50, 50), font=unit_font)

        draw.rectangle([(0, 120), (width, 180)], fill=(0, 38, 84))
        draw.text((50, 135), player_name, fill=(255, 255, 255), font=name_font)

        draw.line([(0, 200), (width, 200)], fill=(0, 0, 0), width=3)
        draw.line([(0, 350), (width, 350)], fill=(0, 0, 0), width=3)

        draw.text((50, 220), stat1.upper(), fill=(0, 0, 0), font=name_font)
        draw.text((50, 280), str(value1), fill=(0, 0, 0), font=stat_font)

        draw.text((50, 370), stat2.upper(), fill=(0, 0, 0), font=name_font)
        draw.text((50, 430), str(value2), fill=(0, 0, 0), font=stat_font)

        img.save(output_path)
        print(f"Saved: {output_path}")

    def generate_stat_images(self):
        player_name, stat_items = self.statcast_dict
        for i in range(0, len(stat_items) - 1, 2):
            stat1, value1 = stat_items[i]
            stat2, value2 = stat_items[i + 1]
            output_filename = f"{self.output_dir}/{stat1.replace(' ', '_')}_{stat2.replace(' ', '_')}.png"
            self.create_statcast_template(stat1, value1, stat2, value2, player_name, output_filename)


class VideoOverlay:
    def __init__(self, video_path, audio_path, images_dir, output_path="temp/output_video.mp4"):
        self.video_path = video_path
        self.audio_path = audio_path
        self.images_dir = images_dir
        self.output_path = output_path
        self.video = VideoFileClip(self.video_path)
        self.image_clips = self._load_images()

    def _load_images(self):
        image_files = [os.path.join(self.images_dir, img) for img in os.listdir(self.images_dir) if img.endswith(('.png', '.jpg', '.jpeg'))]
        images = [ImageClip(img).with_duration(self.video.duration / len(image_files)) for img in image_files]
        return images

    def add_rounded_corners(self, image_clip, radius=20):
        frame = image_clip.get_frame(0)
        pil_image = Image.fromarray(frame)
        mask = Image.new("L", pil_image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([(0, 0), pil_image.size], radius=radius, fill=255)
        pil_image.putalpha(mask)
        return ImageClip(np.array(pil_image))

    def create_image_clips(self):
        for i, img in enumerate(self.image_clips):
            img = img.resized(height=250)
            img = self.add_rounded_corners(img, radius=20)
            img = img.with_position(("left", "bottom"))
            self.image_clips[i] = img

    def overlay_images_on_video(self):
        image_clips = []
        for i, img in enumerate(self.image_clips):
            start_time = i * (self.video.duration / len(self.image_clips))
            end_time = (i + 1) * (self.video.duration / len(self.image_clips))
            img = img.with_start(start_time).with_end(end_time)
            image_clips.append(img)

        final_video = CompositeVideoClip([self.video] + image_clips)
        audio = AudioFileClip(self.audio_path)
        final_video = final_video.with_audio(audio)

        final_video.write_videofile(self.output_path, codec="libx264", fps=24)
        print(f"Video saved to {self.output_path}")