from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse
import os

router = APIRouter()

@router.get("/")
def download_file(file_path: str = Query(..., description="Relative path from project root")):
    print(f"🔍 Requested file path: {file_path}")

    # Sanitize and resolve absolute path
    full_path = os.path.abspath(file_path)

    # Ensure file is inside your allowed folder (to prevent directory traversal)
    allowed_root = os.path.abspath("generated")
    if not full_path.startswith(allowed_root):
        raise HTTPException(status_code=400, detail="Invalid file path")

    print(f"📂 Resolved full path: {full_path}")

    if not os.path.isfile(full_path):
        print("❌ File not found.")
        raise HTTPException(status_code=404, detail="File not found")

    # Set correct media type dynamically (you can refine this later)
    media_type = "audio/mpeg" if full_path.endswith(".mp3") else "image/png"

    return FileResponse(
        full_path,
        media_type=media_type,
        filename=os.path.basename(full_path)
    )
