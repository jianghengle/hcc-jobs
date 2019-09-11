import os

class Squeue(object):
    def __init__(self, username):
        cmd = 'squeue -u ' + username
        self.result = os.popen(cmd).read()

    def json(self):
        return {
            "result": self.result
        }

