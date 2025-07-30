from fastapi import APIRouter, HTTPException, Depends, Body
from pydantic import BaseModel
from app.services.audio_service import generate_audio_file
from app.auth.auth import verify_token
import uuid  # ✅ Add this
import os    # ✅ Also needed
from gtts import gTTS  # ✅ Needed if you're calling it directly here

router = APIRouter()

class AudioRequest(BaseModel):
    text: str
    voice: str = "default"
    language: str = "en"

@router.post("/generate")
def generate_audio_endpoint(payload: AudioRequest):
    try:
        filename = f"audio_{uuid.uuid4().hex}.mp3"
        file_path = f"generated_audio/{filename}"
        os.makedirs("generated_audio", exist_ok=True)
        tts = gTTS(text=payload.text, lang=payload.language)
        tts.save(file_path)
        return {
            "file_path": file_path,
            "download_url": f"/api/v1/download?file_path={file_path}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
