# app/main.py
from fastapi import FastAPI
from app.api.v1 import audio, video, image, ppt, metrics, download
import logging
import os
import sentry_sdk
from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer
from app.api.v1.audio import router as audio_router
from app.api.v1.video import router as video_router
from app.api.v1.image import router as image_router
from app.api.v1.ppt import router as ppt_router
from app.api.v1.metrics import router as metrics_router
from app.api.v1.download import router as download_router

from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBearer



# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

app = FastAPI(
    title="Media Generator API",
    description="Generate audio, video, image, and PPT from text",
    version="1.0.0"
)

app.include_router(audio_router, prefix="/api/v1/audio", tags=["Audio"])
app.include_router(video_router, prefix="/api/v1/video", tags=["Video"])
app.include_router(image_router, prefix="/api/v1/image", tags=["Image"])
app.include_router(ppt_router, prefix="/api/v1/ppt", tags=["PPT"])
app.include_router(metrics_router, prefix="/api/v1/metrics", tags=["Metrics"])
app.include_router(download_router, prefix="/api/v1/download", tags=["Download"])

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("logs/app.log"), logging.StreamHandler()]
)

sentry_sdk.init(dsn="https://a1d84892719d25dca7c04804931d2e82@o4509752680775680.ingest.de.sentry.io/4509752685166672", traces_sample_rate=1.0)


security = HTTPBearer()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Media Generator API",
        version="1.0.0",
        description="Generate audio, video, image, and PPT from text",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "HTTPBearer": {
            "type": "http",
            "scheme": "bearer"
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"HTTPBearer": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
