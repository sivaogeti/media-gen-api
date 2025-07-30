# app/api/v1/video.py
from fastapi import APIRouter, HTTPException, Depends, Body
from pydantic import BaseModel
from app.services.video_service import generate_video_file
from app.auth.auth import verify_token
import uuid  # ✅ Add this
import os    # ✅ Also needed
from gtts import gTTS  # ✅ Needed if you're calling it directly here
from typing import Optional

router = APIRouter()

class VideoInput(BaseModel):
    prompt: str
    tone: str
    domain: str
    environment: str
    transcript: Optional[str] = None  # ✅ make optional

@router.post("/generate")
def generate_video_endpoint(
    payload: VideoInput = Body(...), 
    token: str = Depends(verify_token)):
    try:
        # Use `payload.prompt` as the script
        filename = generate_video_file(
            script=payload.prompt,  # 👈 mapping prompt to script
            duration=10  # Or dynamically set based on text length
        )
        return {
            "message": "Video generated successfully",
            "filename": filename,
            "download_url": f"/api/v1/download?file_path=generated/video/{filename}"
        }
    except Exception as e:
        print("❌ Video generation error:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
