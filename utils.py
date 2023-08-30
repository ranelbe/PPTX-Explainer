import os

main_dir = os.path.dirname(os.path.abspath(__file__))
UPLOADS_FOLDER = os.path.join(main_dir, 'uploads')
OUTPUTS_FOLDER = os.path.join(main_dir, 'outputs')
DB_FOLDER = os.path.join(main_dir, 'DB')

class UploadStatus:
    PENDING = "pending"
    PROCESSING = "processing"
    DONE = "done"
    FAILED = "failed"

def make_directories():
    os.makedirs(UPLOADS_FOLDER, exist_ok=True)
    os.makedirs(OUTPUTS_FOLDER, exist_ok=True)
