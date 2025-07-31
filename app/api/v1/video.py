# app/api/v1/video.py
from fastapi import APIRouter, HTTPException, Depends, Body
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.services.video_service import generate_video_file
from app.auth.auth import verify_token
import os
from typing import Optional

# ✅ Define router FIRST
router = APIRouter()

class VideoInput(BaseModel):
    prompt: str
    tone: str
    domain: str
    environment: str
    transcript: Optional[str] = None

@router.post("/generate")
def generate_video_endpoint(
    payload: VideoInput = Body(...), 
    token: str = Depends(verify_token)
):
    try:
        # Generate video file
        filename = generate_video_file(
            script=payload.prompt,
            duration=10  # Optional: could be dynamic
        )
        video_path = os.path.join("generated/video", filename)

        if not os.path.exists(video_path):
            raise HTTPException(status_code=500, detail="Video not found")

        # ✅ Return the actual file for Streamlit to play
        return FileResponse(
            video_path,
            media_type="video/mp4",
            filename=filename
        )

    except Exception as e:
        print("❌ Video generation error:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
