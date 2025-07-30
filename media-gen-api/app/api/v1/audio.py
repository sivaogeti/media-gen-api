# app/api/v1/audio.py
from fastapi import APIRouter, HTTPException, Query, Depends, Request
from pydantic import BaseModel
from app.services.audio_service import generate_audio_file  # ✅ Only this import
from app.auth.auth import verify_token


router = APIRouter()

class AudioInput(BaseModel):
    text: str
    voice: str = "default"
    language: str = "en"

@router.post("/generate", dependencies=[Depends(verify_token)])
def generate_audio_endpoint(payload: AudioInput):
    try:
        file_path = generate_audio_file(payload.text, payload.voice, payload.language)

        return {
            "status": "success",
            "type": "audio",
            "file_path": file_path,
            "download_url": f"/api/v1/download?file_path={file_path}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
