# app/services/video_service.py

import cv2
import numpy as np
import os
import uuid
import math
from gtts import gTTS
from mutagen.mp3 import MP3
import subprocess

def generate_video_file(script: str, duration: int = None) -> str:
    # Paths
    audio_filename = f"generated/audio/audio_{uuid.uuid4().hex}.mp3"
    raw_video_path = f"generated/video/video_{uuid.uuid4().hex}.mp4"
    final_video_path = raw_video_path.replace(".mp4", "_final.mp4")

    # Ensure directories exist
    os.makedirs(os.path.dirname(audio_filename), exist_ok=True)
    os.makedirs(os.path.dirname(raw_video_path), exist_ok=True)

    # Generate audio
    tts = gTTS(text=script, lang='en')
    tts.save(audio_filename)

    # Get accurate audio duration
    audio = MP3(audio_filename)
    audio_duration = audio.info.length  # e.g., 5.98 seconds

    # Video specs
    fps = 25  # Higher FPS = smoother video
    total_frames = int(audio_duration * fps)
    width, height = 640, 480
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(raw_video_path, fourcc, fps, (width, height))

    # Create each frame
    for _ in range(total_frames):
        frame = np.ones((height, width, 3), dtype=np.uint8) * 255
        cv2.putText(frame, script, (30, height // 2), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
        out.write(frame)

    out.release()

    # Merge audio and video
    ffmpeg_cmd = [
        "ffmpeg",
        "-y",
        "-i", raw_video_path,
        "-i", audio_filename,
        "-c:v", "libx264",
        "-c:a", "aac",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "128k",
        "-shortest",        
        "-movflags", "+faststart",  # 👈 crucial for browser playback
        final_video_path
    ]

    try:
        subprocess.run(ffmpeg_cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg failed: {e}")
        return None

    return os.path.basename(final_video_path)
