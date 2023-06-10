from datetime import datetime
from werkzeug.utils import secure_filename
from utils import OUTPUTS_FOLDER
import uuid
import os
import json

class ErrorMessages:
    """
    Error messages for the web API.
    """
    NO_FILE_ATTACHED = {'upload': 'No file attached'}
    EMPTY_FILENAME = {'upload': 'Empty filename'}
    MISSING_UID = {'status': 'Missing UID parameter'}
    NO_UPLOAD_FOUND = {'status': 'not found'}


def generate_filename(filename: str) -> (str, str):
    """
    Generate a new filename with a unique id and a timestamp.
    :param filename: The original filename.
    :return: The new filename and the generated UID.
    """
    uid = str(uuid.uuid4())
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    base_name, extension = os.path.splitext(secure_filename(filename))
    # remove underscores from the filename if any
    base_name = base_name.replace('_', '')
    new_filename = f"{base_name}_{timestamp}_{uid}{extension}"
    return new_filename, uid


def load_explanation(filename: str) -> (str, str):
    """
    Load the explanation from the output file if it exists.
    :param filename: The filename of the uploaded file.
    :return: Explanation if it exists, None otherwise.
    And the status message (done or pending).
    """
    output_path = os.path.join(OUTPUTS_FOLDER,
                               os.path.splitext(filename)[0] + '.json')
    if os.path.exists(output_path):
        with open(output_path, 'r') as file:
            explanation = json.load(file)
        status_msg = 'done'
    else:
        explanation = None
        status_msg = 'pending'
    return explanation, status_msg
