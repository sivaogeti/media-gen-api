import os
import shutil
from datetime import datetime

SOURCE_DIR = "generated"
ARCHIVE_DIR = f"archive_{datetime.now().strftime('%Y%m%d_%H%M')}"

def archive_all():
    if not os.path.exists(SOURCE_DIR):
        print("No content to archive.")
        return

    shutil.copytree(SOURCE_DIR, ARCHIVE_DIR)
    print(f"Archived to {ARCHIVE_DIR}")

if __name__ == "__main__":
    archive_all()
