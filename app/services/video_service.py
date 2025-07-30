# app/services/video_service.py
import os
from datetime import datetime
from app.db import SessionLocal
from app.models import MediaGeneration
import logging
logger = logging.getLogger(__name__)

def generate_video_file(script: str, duration: int = 10) -> str:
    try:
        # Simulate saving a generated video file
        filename = f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        folder = "generated/video"
        os.makedirs(folder, exist_ok=True)
    
        # Placeholder: Simulate video generation by writing script info to a file
        with open(os.path.join(folder, filename), "w") as f:
            f.write(f"Script: {script}\nDuration: {duration} seconds")
        logger.info(f"Generated Video: {filename}")
        return filename
    except:
        logger.error(f"Video generation failed: {str(e)}")
        raise
    

def save_metadata(media_type, prompt, file_path):
    db = SessionLocal()
    record = MediaGeneration(
        media_type=media_type,
        prompt=prompt,
        file_path=file_path,
    )
    db.add(record)
    db.commit()
    db.close()