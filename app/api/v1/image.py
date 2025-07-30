from fastapi import APIRouter, HTTPException, Depends, Body
from pydantic import BaseModel
from app.auth.auth import verify_token
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import os

router = APIRouter()

class ImageRequest(BaseModel):
    prompt: str
    style: str = "default"

class ImageResponse(BaseModel):
    message: str
    filename: str
    download_url: str

@router.post("/generate", response_model=ImageResponse)
def generate_image_file_endpoint(
    data: ImageRequest = Body(...),
    token: str = Depends(verify_token)
):
    prompt = data.prompt
    style = data.style
    filename = f"image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    folder = "generated/image"
    os.makedirs(folder, exist_ok=True)
    output_path = os.path.join(folder, filename)

    try:
        img = Image.new("RGB", (768, 512), color="white")
        draw = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.load_default()

        draw.text((20, 20), f"Prompt: {prompt}", fill="black", font=font)
        draw.text((20, 60), f"Style: {style}", fill="gray", font=font)

        img.save(output_path, format="PNG")

        print(f"✅ Image created: {output_path}, size = {os.path.getsize(output_path)} bytes")
        return {
            "message": "Image generated successfully",
            "filename": filename,
            "download_url": f"/api/v1/download?file_path=generated/image/{filename}"
        }

    except Exception as e:
        print(f"❌ Image generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
