from flask import Flask, request, jsonify
from utils import UPLOADS_FOLDER, make_directories
from web_api_utils import load_explanation, ErrorMessages, \
    save_to_db, fetch_upload
import json


app = Flask(__name__)
app.config['UPLOADS_FOLDER'] = UPLOADS_FOLDER


@app.route('/upload', methods=['POST'])
def upload() -> json:
    """
    Route to handle file upload post requests.
    Saves the given file in the 'uploads' folder and updates the DB.
    :return: JSON object with the generated UID of the uploaded file.
    """
    # check if the post request has a file part
    if 'file' not in request.files:
        return jsonify(ErrorMessages.NO_FILE_ATTACHED), 400

    file = request.files['file']
    # check if the filename is missing
    if file.filename == '':
        return jsonify(ErrorMessages.EMPTY_FILENAME), 400

    try:
        email = request.form.get('email')  # might be None
        upload_obj = save_to_db(file.filename, email)  # save to db
        file.save(upload_obj.upload_path)  # save to uploads folder
    except Exception as e:
        return jsonify({'upload': str(e)}), 500

    # return the UID of the uploaded file
    return jsonify({'uid': upload_obj.uid})


@app.route('/status', methods=['GET'])
def status() -> json:
    """
    Route to handle status get requests.
    :return: JSON object with the available information about the upload.
    """
    try:
        # get the parameters from the request (might be None)
        uid = request.args.get('uid')
        filename = request.args.get('filename')
        email = request.args.get('email')

        # search for the upload in the database
        upload_obj = fetch_upload(uid=uid, filename=filename, email=email)

        # load the explanation if exists
        explanation = load_explanation(upload_obj.output_path)

    except Exception as e:
        return jsonify({'status': str(e)}), 500

    return jsonify({
        'uid': upload_obj.uid,
        'filename': upload_obj.filename,
        'user_id': upload_obj.user_id,
        'upload_time': upload_obj.upload_time,
        'finish_time': upload_obj.finish_time,
        'status': upload_obj.status,
        'explanation': explanation
    })


if __name__ == '__main__':
    make_directories()
    app.run()
