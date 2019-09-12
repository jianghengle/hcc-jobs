import os
from datetime import datetime

class Squeue(object):
    def __init__(self, username):
        cmd = 'squeue -u ' + username
        self.result = os.popen(cmd).read().strip()
        now = datetime.now()
        self.timestamp = datetime.timestamp(now)

    def json(self):
        return {
            "timestamp": self.timestamp,
            "result": self.result
        }

class JobDetail(object):
    def __init__(self, username, job_id):
        fields = 'JobID,JobName,Partition,Account,User,State,ExitCode,Elapsed,ReqCPUS,AllocCPUs,ReqMem,ReqNodes,AllocNodes,NodeList'
        self.fields = fields.split(',')
        cmd = 'sacct -j ' + job_id + ' -p -X -n -o ' + fields
        self.values = os.popen(cmd).read().strip().split('|')
        self.values.pop()
        if self.values[4] != username:
            raise Exception('permission denied.')

        now = datetime.now()
        self.timestamp = datetime.timestamp(now)


    def json(self):
        return {
            "timestamp": self.timestamp,
            "fields": self.fields,
            "values": self.values
        }