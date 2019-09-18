import os
from datetime import datetime
import threading


class Jobs(object):
    def __init__(self, user, start_date):
        fields = 'JobID,JobName,State,Start,Elapsed,AllocNodes'
        self.fields = fields.split(',')
        cmd = 'sacct -u ' + user.username + ' -S ' + start_date + ' -p -X -n -o ' + fields
        self.values = os.popen(cmd).read().strip().split('\n')
        now = datetime.now()
        self.timestamp = datetime.timestamp(now)

    def json(self):
        return {
            "timestamp": self.timestamp,
            "fields": self.fields,
            "values": self.values,
        }


class JobDetail(object):
    def __init__(self, user, job_id):
        self.user = user
        self.job_id = job_id
        fields = 'JobID,JobName,Partition,Account,User,State,Start,End,Elapsed,ReqCPUS,AllocCPUs,ReqMem,ReqNodes,AllocNodes,NodeList'
        self.fields = fields.split(',')
        cmd = 'sacct -j ' + job_id + ' -p -X -n -o ' + fields
        self.values = os.popen(cmd).read().strip().split('|')
        self.values.pop()
        if self.values[4] != user.username:
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
            t = threading.Thread(target=top_on_node, args=(self.user, self.job_id, node, self.nodes), daemon=True)
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


def top_on_node(user, job_id, node, nodes):
    cmd = 'srun --pty --jobid ' + job_id + ' -w ' + node + ' top -u ' + user.username + ' -n 1 -b'
    result = user.run_command(cmd)
    nodes[node] = result
