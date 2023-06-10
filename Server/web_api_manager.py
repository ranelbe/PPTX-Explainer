from flask import Flask, request, jsonify
from utils import UPLOADS_FOLDER, make_directories
from web_api_utils import generate_filename, \
    load_explanation, ErrorMessages
import os
import glob
import json

app = Flask(__name__)
app.config['UPLOADS_FOLDER'] = UPLOADS_FOLDER


@app.route('/upload', methods=['POST'])
def upload() -> json:
    """
    Route to handle file upload post requests.
    This route saves the given file in the 'uploads' folder.
    :return: JSON object with the generated UID of the uploaded file.
    """
    # check if the post request has a file part
    if 'file' not in request.files:
        return jsonify(ErrorMessages.NO_FILE_ATTACHED), 400

    file = request.files['file']
    # check if the filename is missing
    if file.filename == '':
        return jsonify(ErrorMessages.EMPTY_FILENAME), 400

    new_filename, uid = generate_filename(file.filename)

    # save the file in the 'uploads' folder
    file_path = os.path.join(app.config['UPLOADS_FOLDER'], new_filename)
    file.save(file_path)

    return jsonify({'uid': uid})


@app.route('/status/<uid>', methods=['GET'])
@app.route('/status/', methods=['GET'])
def status(uid=None) -> json:
    """
    Route to handle status get requests.
    :param uid: The unique ID of the uploaded file.
    :return: JSON object with the available information about the upload.
    """
    # check if the uid parameter is missing
    if not uid:
        return jsonify(ErrorMessages.MISSING_UID), 400

    # search for the file with the given uid in the 'uploads' folder
    uploads = glob.glob(os.path.join(
        app.config['UPLOADS_FOLDER'], '**', f"*{uid}*"),
        recursive=True
    )

    if not uploads:
        return jsonify(ErrorMessages.NO_UPLOAD_FOUND), 404

    # file was found extract the original filename and the timestamp
    file_path = uploads[0]
    filename = os.path.basename(file_path)
    original_filename, timestamp = filename.split('_')[0:2]
    explanation, status_msg = load_explanation(filename)

    return jsonify({
        'status': status_msg,
        'filename': original_filename,
        'timestamp': timestamp,
        'explanation': explanation
    })

if __name__ == '__main__':
    make_directories()
    app.run()
