from fastapi import APIRouter, HTTPException, Depends, Body
from fastapi.responses import Response
from pydantic import BaseModel
from app.auth.auth import verify_token
import requests
import os
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()


# ✅ Define router
router = APIRouter()

# ✅ Define Request schema
class ImageRequest(BaseModel):
    prompt: str
    style: str = "default"

UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")  # store this in .env
print(f"unsplash key is: {UNSPLASH_ACCESS_KEY}")

# ✅ Endpoint
@router.post("/generate")
def generate_image_file_endpoint(
    data: ImageRequest = Body(...),
    token: str = Depends(verify_token)
):
    query = f"{data.prompt} {data.style}"
    url = f"https://api.unsplash.com/photos/random?query={query}&client_id={UNSPLASH_ACCESS_KEY}&orientation=landscape"

    try:
        r = requests.get(url)
        r.raise_for_status()
        image_url = r.json()["urls"]["regular"]
        img_data = requests.get(image_url).content
        return Response(content=img_data, media_type="image/jpeg")

    except Exception as e:
        print(f"❌ Image fetch failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Image generation failed.")
