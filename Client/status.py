class Status:
    """
    Class to represent the available information of an uploaded file.
    """
    def __init__(self, data):
        self.uid = data.get('uid')
        self.filename = data.get('filename')
        self.user_id = data.get('user_id')
        self.upload_time = data.get('upload_time')
        self.finish_time = data.get('finish_time')
        self.status = data.get('status')
        self.explanation = data.get('explanation')

    def __str__(self):
        return f"""
        ============== Status =============
        UID: {self.uid}
        Filename: {self.filename}
        User ID: {self.user_id}
        Upload Time: {self.upload_time}
        Finish Time: {self.finish_time}
        Status: {self.status}
        Explanation: {self.explanation}\n"""
