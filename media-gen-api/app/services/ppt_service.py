# app/services/ppt_service.py
import os
from datetime import datetime
from app.db import SessionLocal
from app.models import MediaGeneration
import logging
logger = logging.getLogger(__name__)

def generate_ppt_file(slides: list[dict]) -> str:
    try:
        filename = f"ppt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.ppt"
        folder = "generated/ppt"
        os.makedirs(folder, exist_ok=True)
    
        with open(os.path.join(folder, filename), "w") as f:
            for i, slide in enumerate(slides, 1):
                f.write(f"Slide {i}:\nTitle: {slide['title']}\nContent: {slide['content']}\n\n")
        logger.info(f"Generated PPT: {filename}")
        return filename
    except:
        logger.error(f"PPT Generation failed: {str(e)}")
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