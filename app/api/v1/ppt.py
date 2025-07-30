# app/api/v1/ppt.py
from fastapi import APIRouter, HTTPException, Query, Depends, Request
from pydantic import BaseModel
from typing import List
from app.services.ppt_service import generate_ppt_file
from app.auth.auth import verify_token

router = APIRouter()

class Slide(BaseModel):
    title: str
    content: str

class PPTInput(BaseModel):
    slides: List[Slide]

@router.post("/generate")
def generate_ppt(payload: PPTInput):
    filename = generate_ppt_file([slide.dict() for slide in payload.slides])
    return {
        "message": "PPT generated successfully",
        "filename": filename,
        "download_url": f"/api/v1/download?file_path=generated/ppt/{filename}"
    }
