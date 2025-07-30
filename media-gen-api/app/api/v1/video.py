from fastapi import APIRouter, HTTPException, Query, Depends, Request
from pydantic import BaseModel
from app.services.video_service import generate_video_file
from app.auth.auth import verify_token


router = APIRouter()

class VideoInput(BaseModel):
    script: str
    duration: int = 10

@router.post("/generate", dependencies=[Depends(verify_token)])  # ✅ FIX: POST, not GET
def generate_video(payload: VideoInput):
    filename = generate_video_file(payload.script, payload.duration)
    return {
        "message": "Video generated successfully",
        "filename": filename,
        "download_url": f"/api/v1/download?file_path=generated/video/{filename}"
    }
