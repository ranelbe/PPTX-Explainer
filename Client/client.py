from Client.status import Status
from requests import HTTPError
import requests

base_url = "http://127.0.0.1:5000/"

def upload() -> str:
    """
    Upload a file to the server.
    :return: The UID of the uploaded file.
    :raises: HTTPError if the response contains an error code.
    """
    try:
        file_path = input("Enter the file path: ")
        files = {'file': open(file_path, 'rb')}
        response = requests.post(base_url + 'upload', files=files)
        response.raise_for_status()
        return response.json().get('uid')
    except HTTPError as e:
        print(e.response.json().get('status'))
    except Exception as e:
        print(e)


def get_status() -> Status:
    """
    Get the status of an uploaded file.
    :return: The status of the uploaded file.
    :raises: HTTPError if the response contains an error code.
    """
    try:
        uid = input("Enter a UID: ")
        response = requests.get(base_url + f'status/{uid}')
        response.raise_for_status()
        return Status(response.json())
    except HTTPError as e:
        print(e.response.json().get('status'))
    except Exception as e:
        print(e)


def main():
    while True:
        print("Options:")
        print("1. Upload a file")
        print("2. Check status")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")
        if choice == "1":
            uid = upload()
            if uid:
                print(f"File uploaded successfully.\nUID: {uid}")
        elif choice == "2":
            status = get_status()
            if status:
                print(f"The status of the given upload is:\n{status}")
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
