from Client.status import Status
from requests import HTTPError
import requests

base_url = "http://127.0.0.1:5000/"

def upload(file_path, email=None) -> str:
    """
    Upload a file to the server.
    :param file_path: The path to the file.
    :param email: email address of the user (optional).
    :return: The UID of the uploaded file.
    :raises: HTTPError if the response contains an error code.
    """
    try:
        files = {'file': open(file_path, 'rb')}
        data = {'email': email} if email else {}
        response = requests.post(base_url + 'upload', files=files, data=data)
        response.raise_for_status()
        return response.json().get('uid')
    except HTTPError as e:
        print(e.response.json().get('status'))
    except Exception as e:
        print(e)


def get_status(uid=None, filename=None, email=None) -> Status:
    """
    Get the status of an uploaded file.
    :param uid: The UID of the uploaded file (optional).
    :param filename: The filename of the uploaded file (optional).
    :param email: email address of the user (optional).
    :return: The status of the uploaded file.
    :raises: HTTPError if the response contains an error code.
    """
    try:
        params = {}
        if uid:
            params = {'uid': uid}
        elif filename and email:
            params = {'filename': filename, 'email': email}
        response = requests.get(base_url + 'status', params=params)
        response.raise_for_status()
        return Status(response.json())
    except HTTPError as e:
        print(e.response.json().get('status'))
    except Exception as e:
        print(e)
