import os

class Squeue(object):
    def __init__(self, username):
        self.username = username
        cmd = 'squeue -u ' + username + ' -l'
        self.result = os.popen(cmd).read()

    def json(self):
        return {
            "username": self.username,
            "result": self.result,
        }

