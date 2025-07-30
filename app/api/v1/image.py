from fastapi import APIRouter, HTTPException, Query, Depends, Request
from pydantic import BaseModel
from app.services.image_service import generate_image_file
from app.auth.auth import verify_token

router = APIRouter()

class ImageInput(BaseModel):
    prompt: str
    style: str = "default"

@router.post("/generate", dependencies=[Depends(verify_token)])  # ✅ FIX: POST, not GET
def generate_image(payload: ImageInput):
    filename = generate_image_file(payload.prompt, payload.style)
    return {
        "message": "Image generated successfully",
        "filename": filename,
        "download_url": f"/api/v1/download?file_path=generated/image/{filename}"
    }
