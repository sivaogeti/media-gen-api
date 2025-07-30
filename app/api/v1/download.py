from fastapi import APIRouter, HTTPException, Query, Depends, Request
from fastapi.responses import FileResponse
from app.auth.auth import verify_token
import os

router = APIRouter()

@router.get("/", dependencies=[Depends(verify_token)])
def download_file(file_path: str = Query(..., description="Relative path from project root")):
    # Sanitize the input path
    file_path = os.path.normpath(file_path)

    # Absolute path (from project root)
    abs_path = os.path.join(os.getcwd(), file_path)

    if not os.path.isfile(abs_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=abs_path,
        filename=os.path.basename(abs_path),
        media_type='application/octet-stream'
    )
