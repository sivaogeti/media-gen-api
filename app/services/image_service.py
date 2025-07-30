# app/services/image_service.py
import os
from datetime import datetime
from app.db import SessionLocal
from app.models import MediaGeneration
import logging
logger = logging.getLogger(__name__)


def generate_image_file(prompt: str, style: str = "default") -> str:
    try:
        # Simulate saving a generated image file
        filename = f"image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        folder = "generated/image"
        os.makedirs(folder, exist_ok=True)
    
        # Placeholder: Simulate image generation by writing prompt text to a file
        with open(os.path.join(folder, filename), "w") as f:
            f.write(f"Prompt: {prompt}\nStyle: {style}")
        logger.info(f"Generated Image: {filename}")
        if os.path.isfile(output_path):
            print(f"✅ Image created: {output_path}, size = {os.path.getsize(output_path)} bytes")
        else:
            print(f"❌ Image file not found at: {output_path}")
        return filename
    except:
        logger.error(f"Image Geneartion failed: {str(e)}")
        raise

from app.db import SessionLocal
from app.models import MediaGeneration

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
