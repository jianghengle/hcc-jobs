import os
from datetime import datetime

class Squeue(object):
    def __init__(self, username):
        cmd = 'squeue -u ' + username
        self.result = os.popen(cmd).read()
        now = datetime.now()
        self.timestamp = datetime.timestamp(now)

    def json(self):
        return {
        	"timestamp": self.timestamp,
            "result": self.result
        }

