# app/main.py
from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer
from fastapi import Security

from fastapi import FastAPI

from app.api.v1.audio import router as audio_router
from app.api.v1.video import router as video_router
from app.api.v1.image import router as image_router
from app.api.v1.ppt import router as ppt_router
from app.api.v1.metrics import router as metrics_router
from app.api.v1.download import router as download_router
from fastapi import Security

from app.auth.auth import verify_token

bearer_scheme = HTTPBearer()


app = FastAPI(
    title="Media Generation API",
    description="Generate audio, video, image, and PPT content via secure endpoints.",
    version="1.0.0"
)

# Root for health check
@app.get("/")
def root():
    return {"message": "FastAPI running successfully!"}

# Registering route modules
app.include_router(audio_router, prefix="/api/v1/audio", tags=["Audio"], dependencies=[Depends(verify_token)])
app.include_router(video_router, prefix="/api/v1/video", tags=["Video"], dependencies=[Depends(verify_token)])
app.include_router(image_router, prefix="/api/v1/image", tags=["Image"], dependencies=[Depends(verify_token)])
app.include_router(ppt_router, prefix="/api/v1/ppt", tags=["PPT"], dependencies=[Depends(verify_token)])
app.include_router(metrics_router, prefix="/api/v1/metrics", tags=["Metrics"], dependencies=[Depends(verify_token)])
app.include_router(download_router, prefix="/api/v1/download", tags=["Download"])

