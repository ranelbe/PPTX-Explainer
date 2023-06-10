import os
import subprocess
import sys
import time
from unittest import TestCase
from Client.client import upload, get_status

main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVER = os.path.join(main_dir, 'Server', 'web_api_manager.py')
EXPLAINER = os.path.join(main_dir, 'Explainer', 'pptx_explainer.py')
PPTX_PATH = 'pptx_files/test.pptx'


class Test(TestCase):
    """ Testing the code. """

    def setUp(self):
        """ Start the server and the explainer. """
        self.start_server()
        self.start_explainer()
        self.filename = os.path.basename(os.path.splitext(PPTX_PATH)[0])
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
        uid = upload(PPTX_PATH)
        print(uid)
        self.assertIsNotNone(uid)
        time.sleep(10)

        # check the status of the uploaded file.
        status = get_status(uid)
        print(status)
        self.assertIsNotNone(status)
        self.assertTrue(status.is_pending())
        self.assertEqual(status.filename, self.filename)
        self.assertIsNotNone(status.timestamp)
        self.assertIsNone(status.explanation)

        # wait for the file to be processed.
        time.sleep(110)
        status = get_status(uid)
        print(status)
        self.assertTrue(status.is_done())
        self.assertEqual(status.filename, self.filename)
        self.assertIsNotNone(status.timestamp)
        self.assertIsNotNone(status.explanation)
