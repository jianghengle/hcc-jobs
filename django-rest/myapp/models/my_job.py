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
        self.username = username
        self.job_id = job_id
        fields = 'JobID,JobName,Partition,Account,User,State,ExitCode,Elapsed,ReqCPUS,AllocCPUs,ReqMem,ReqNodes,AllocNodes,NodeList'
        self.fields = fields.split(',')
        cmd = 'sacct -j ' + job_id + ' -p -X -n -o ' + fields
        self.values = os.popen(cmd).read().strip().split('|')
        self.values.pop()
        if self.values[4] != username:
            raise Exception('permission denied.')

        self.nodes = {}
        if self.values[5] == 'RUNNING':
            self.collect_nodes()

        now = datetime.now()
        self.timestamp = datetime.timestamp(now)

    def collect_nodes(self):
        nodes_value = self.values[len(self.values) - 1]
        idx = nodes_value.find('[')
        if (idx != -1):
            prefix = nodes_value[0:idx]
            nums = nodes_value[(idx+1):(-1)].split(',')
            nodes = [(prefix + n) for n in nums]
        else:
            nodes = [nodes_value]

        threads = []
        for node in nodes:
            t = threading.Thread(target=top_on_node, args=(self.username, self.job_id, node, self.nodes), daemon=True)
            threads.append(t)
            t.start()
        for t in threads:
            t.join()

    def json(self):
        return {
            "timestamp": self.timestamp,
            "fields": self.fields,
            "values": self.values,
            "nodes": self.nodes
        }


def top_on_node(username, job_id, node, nodes):
    cmd = "sudo runuser -l " + username + " -c 'srun --pty --jobid " + job_id + " -w " + node + " top -u " + username + " -n 1 -b'"
    result = os.popen(cmd).read().strip()
    nodes[node] = result
