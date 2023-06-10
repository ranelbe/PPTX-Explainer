from Client.status import Status
from requests import HTTPError
import requests

base_url = "http://127.0.0.1:5000/"

def upload(file_path) -> str:
    """
    Upload a file to the server.
    :param file_path: The path to the file.
    :return: The UID of the uploaded file.
    :raises: HTTPError if the response contains an error code.
    """
    try:
        files = {'file': open(file_path, 'rb')}
        response = requests.post(base_url + 'upload', files=files)
        response.raise_for_status()
        return response.json().get('uid')
    except HTTPError as e:
        print(e.response.json().get('status'))
    except Exception as e:
        print(e)


def get_status(uid) -> Status:
    """
    Get the status of an uploaded file.
    :param uid: The UID of the uploaded file.
    :return: The status of the uploaded file.
    :raises: HTTPError if the response contains an error code.
    """
    try:
        response = requests.get(base_url + f'status/{uid}')
        response.raise_for_status()
        return Status(response.json())
    except HTTPError as e:
        print(e.response.json().get('status'))
    except Exception as e:
        print(e)
