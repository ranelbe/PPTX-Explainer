class Status:
    """
    Class to represent the available information of an uploaded file.
    status, filename, timestamp, explanation.
    """
    def __init__(self, data):
        self.status = data.get('status')
        self.filename = data.get('filename')
        self.timestamp = data.get('timestamp')
        self.explanation = data.get('explanation')

    def __str__(self):
        return f"""
        ============== Status =============
        Status: {self.status}
        Filename: {self.filename}
        Timestamp: {self.timestamp}
        Explanation: {self.explanation}\n"""

    def is_done(self):
        """ Check if the status is done. """
        return self.status == 'done'

    def is_pending(self):
        """ Check if the status is pending. """
        return self.status == 'pending'
