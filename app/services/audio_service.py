# app/services/audio_service.py
from gtts import gTTS
import os
from datetime import datetime
from app.db import SessionLocal
from app.models import MediaGeneration
import logging
logger = logging.getLogger(__name__)
import uuid

def generate_audio_file(text: str, voice: str = "default", language: str = "en") -> str:
    try:
        tts = gTTS(text=text, lang=language, slow=False)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"audio_{timestamp}.mp3"
        output_dir = "generated/audio"
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, filename)
        tts.save(file_path)
        logger.info(f"Generated Audio: {filename}")
        return file_path
    except:
        logger.error(f"Audio Generation Failed: {str(e)}")
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
