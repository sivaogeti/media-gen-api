from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import Response  # ✅ add this
from pydantic import BaseModel
from gtts import gTTS
import uuid
import os
router = APIRouter()

class AudioRequest(BaseModel):
    text: str
    voice: str = "default"
    language: str = "en"

@router.post("/generate")
def generate_audio_endpoint(payload: AudioRequest):
    try:
        # ✅ Save inside generated/audio for consistency
        filename = f"audio_{uuid.uuid4().hex}.mp3"
        folder = "generated/audio"
        os.makedirs("generated_audio", exist_ok=True)
        file_path = f"generated_audio/{filename}" # ✅ match your video & image folders        
        
        # ✅ Generate TTS audio
        tts = gTTS(text=payload.text, lang=payload.language)
        tts.save(file_path)
        
        # ✅ Return audio bytes for inline Streamlit playback
        with open(file_path, "rb") as f:
            audio_bytes = f.read()

        return Response(content=audio_bytes, media_type="audio/mpeg")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
