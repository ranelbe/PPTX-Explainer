import os

main_dir = os.path.dirname(os.path.abspath(__file__))
UPLOADS_FOLDER = os.path.join(main_dir, 'uploads')
PROCESSED_FOLDER = os.path.join(UPLOADS_FOLDER, 'processed')
OUTPUTS_FOLDER = os.path.join(main_dir, 'outputs')


def make_directories():
    os.makedirs(UPLOADS_FOLDER, exist_ok=True)
    os.makedirs(PROCESSED_FOLDER, exist_ok=True)
    os.makedirs(OUTPUTS_FOLDER, exist_ok=True)
