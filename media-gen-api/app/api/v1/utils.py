# app/api/v1/utils.py
from fastapi.responses import FileResponse

def download_file(file_path: str):
    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )
