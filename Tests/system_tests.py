import os
import subprocess
import sys
import time
from unittest import TestCase
from Client.client import upload, get_status
from utils import UploadStatus

main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVER = os.path.join(main_dir, 'Server', 'web_api_manager.py')
EXPLAINER = os.path.join(main_dir, 'Explainer', 'pptx_explainer.py')
FILE_NAME = 'test.pptx'
PPTX_PATH = f'pptx_files/{FILE_NAME}'
USER_EMAIL = 'ranelbe@gmail.com'


class Test(TestCase):
    """ Testing the code. """

    def setUp(self):
        """ Start the server and the explainer. """
        self.start_server()
        self.start_explainer()
        self.filename = PPTX_PATH
        time.sleep(5)

    def tearDown(self):
        """ Kill the server and the explainer. """
        self.server.kill()
        self.explainer.kill()

    def start_server(self):
        """ Start the server. """
        self.server = subprocess.Popen([sys.executable, SERVER])

    def start_explainer(self):
        """ Start the explainer. """
        self.explainer = subprocess.Popen([sys.executable, EXPLAINER])

    def test_upload_and_status(self):
        """ Test the upload and status of a file. """

        # upload a file and get the uid.
        uid = upload(PPTX_PATH, USER_EMAIL)
        print(uid)
        self.assertIsNotNone(uid)
        time.sleep(10)

        # check the status of the uploaded file.
        status = get_status(uid=uid)
        print(status)
        self.assertIsNotNone(status)
        self.assertEqual(status.filename, FILE_NAME)
        self.assertIsNotNone(status.user_id)
        self.assertTrue(status.status in [UploadStatus.PENDING, UploadStatus.PROCESSING])
        self.assertIsNotNone(status.upload_time)
        self.assertIsNone(status.finish_time)
        self.assertIsNone(status.explanation)

        # wait for the file to be processed.
        time.sleep(70)
        status = get_status(filename=FILE_NAME, email=USER_EMAIL)
        print(status)
        self.assertIsNotNone(status)
        self.assertEqual(status.filename, FILE_NAME)
        self.assertIsNotNone(status.user_id)
        self.assertEqual(status.status, UploadStatus.DONE)
        self.assertIsNotNone(status.upload_time)
        self.assertIsNotNone(status.finish_time)
        self.assertIsNotNone(status.explanation)
