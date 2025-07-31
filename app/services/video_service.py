# app/services/video_service.py

import os
import uuid
import requests
from gtts import gTTS
from mutagen.mp3 import MP3
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
from dotenv import load_dotenv

load_dotenv()

UNSPLASH_KEY = os.getenv("UNSPLASH_ACCESS_KEY")
UNSPLASH_API = "https://api.unsplash.com/photos/random"

def fetch_unsplash_images(query, count=3):
    headers = {"Accept-Version": "v1", "Authorization": f"Client-ID {UNSPLASH_KEY}"}
    urls = []

    for _ in range(count):
        r = requests.get(UNSPLASH_API, params={"query": query}, headers=headers)
        if r.status_code == 200:
            data = r.json()
            if isinstance(data, dict):
                urls.append(data["urls"]["regular"])
            elif isinstance(data, list) and len(data) > 0:
                urls.append(data[0]["urls"]["regular"])
    return urls

def generate_video_file(script: str, duration: int = None) -> str:
    os.makedirs("generated/video", exist_ok=True)
    os.makedirs("generated/audio", exist_ok=True)
    os.makedirs("generated/tmp", exist_ok=True)

    video_filename = f"video_{uuid.uuid4().hex}.mp4"
    video_path = os.path.join("generated/video", video_filename)
    audio_path = f"generated/audio/audio_{uuid.uuid4().hex}.mp3"

    # Step 1: Generate audio
    tts = gTTS(text=script, lang='en')
    tts.save(audio_path)

    # Get audio duration (fallback if 0)
    audio = MP3(audio_path)
    audio_duration = max(audio.info.length, 3.0)  # ensure at least 3s

    # Step 2: Fetch Unsplash images
    images = fetch_unsplash_images(script, count=3)
    if not images:
        raise Exception("No images found from Unsplash for the prompt")

    # Step 3: Create slideshow clips
    clips = []
    per_image_duration = audio_duration / len(images)
    tmp_files = []

    for url in images:
        img_data = requests.get(url).content
        tmp_file = f"generated/tmp/tmp_{uuid.uuid4().hex}.jpg"
        tmp_files.append(tmp_file)

        with open(tmp_file, "wb") as f:
            f.write(img_data)

        clip = ImageClip(tmp_file).resize(height=720).set_duration(per_image_duration)
        clips.append(clip)

    # Step 4: Concatenate without negative padding
    final_clip = concatenate_videoclips(clips, method="compose")

    # Step 5: Force duration to match audio
    final_clip = final_clip.set_duration(audio_duration)

    # Step 6: Add audio
    final_clip = final_clip.set_audio(AudioFileClip(audio_path))

    # Step 7: Export video
    final_clip.write_videofile(
        video_path,
        fps=24,
        codec="libx264",
        audio_codec="aac",
        threads=4,
        preset="ultrafast"
    )

    # Cleanup
    for file in tmp_files:
        try:
            os.remove(file)
        except:
            pass

    return video_filename
