from datetime import datetime
from sqlalchemy.orm import Session
from DB.database import engine, Upload, User
import uuid
import os
import json


class ErrorMessages:
    """
    Error messages for the web API.
    """
    NO_FILE_ATTACHED = {'upload': 'No file attached'}
    EMPTY_FILENAME = {'upload': 'Empty filename'}
    NO_UPLOAD_FOUND = 'upload not found'
    USER_NOT_FOUND = 'user not found'
    MISSING_PARAMETERS = 'uid or filename and email are required'


def save_to_db(filename: str, email: str) -> Upload:
    """
    Save the upload to the database.
    :param filename: The filename of the uploaded file.
    :param email: The email of the user.
    :return: The upload object.
    """
    with Session(engine) as session:
        # create the upload object
        upload_obj = Upload(
            uid=uuid.uuid4(),
            filename=filename,
            upload_time=datetime.now()
        )
        if email:
            # fetch the user from the database if exists
            user = session.query(User).filter(User.email == email).first()
            if not user:
                user = User(email=email)  # create new user
                session.add(user)
                session.commit()
            # associate the user with the new upload
            upload_obj.user_id = user.id

        # commit the changes to the database
        session.merge(upload_obj)
        session.commit()

    return upload_obj


def fetch_upload(uid: str, filename: str, email: str):
    """
    Fetch the upload from the database.
    :param uid: the uid of the upload.
    :param filename: the filename of the upload.
    :param email: the email of the user.
    :return: The upload object if exists.
    """
    with Session(engine) as session:
        if uid:
            # fetch the upload with the given uid from the database
            upload = session.query(Upload).filter_by(uid=uuid.UUID(uid)).first()
        elif filename and email:
            # fetch the upload with the given filename and email from the database
            user = session.query(User).filter_by(email=email).first()
            if not user:
                raise ValueError(ErrorMessages.USER_NOT_FOUND)
            upload = session.query(Upload). \
                filter_by(user_id=user.id, filename=filename). \
                order_by(Upload.upload_time.desc()).first()
        else:
            raise ValueError(ErrorMessages.MISSING_PARAMETERS)

        if not upload:
            # can't find the upload in the database
            raise ValueError(ErrorMessages.NO_UPLOAD_FOUND)

        return upload


def load_explanation(output_path: str):
    """
    Load the explanation from the output file if it exists.
    :param output_path: The path to the output file.
    :return: Explanation if it exists, None otherwise.
    """
    if os.path.exists(output_path):
        with open(output_path, 'r') as file:
            return json.load(file)
    return None
