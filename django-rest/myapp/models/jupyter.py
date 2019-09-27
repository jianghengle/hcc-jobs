import threading
import time
import subprocess
from django.db import models
from django.utils import timezone
from django.conf import settings
from random import randint
from .helpers import random_string_digits


class Jupyter(models.Model):
    cluster = models.CharField(max_length=128)
    username = models.CharField(max_length=128)
    token = models.CharField(db_index=True, max_length=128)
    port = models.IntegerField()
    pid = models.IntegerField()
    started_at = models.DateTimeField('started at')

    def json(self):
        return {
            'id': self.id,
            'cluster': self.cluster,
            'username': self.username,
            'token': self.token,
            'port': self.port,
            'pid': self.pid,
            'startedAt': self.started_at.timestamp()
        }

    @staticmethod
    def create(cluster, user):
        jupyter = Jupyter()
        jupyter.cluster = cluster
        jupyter.username = user.username
        jupyter.token = random_string_digits(48)
        jupyter.port = pick_port(cluster)
        jupyter.pid = 0
        jupyter.started_at = timezone.now()
        jupyter.save()

        # start jupyter server
        t = threading.Thread(target=start_jupyter_server, args=(user, jupyter), daemon=True)
        t.start()
        time.sleep(3)
        return jupyter

    @staticmethod
    def stop(user, jupyter_id):
        jupyter = Jupyter.objects.get(pk=jupyter_id)
        jupyter.delete()

        # stop jupyter server
        stop_jupyter_server(user, jupyter)
        return jupyter

    @staticmethod
    def get_by_user(cluster, user):
        return list(Jupyter.objects.filter(cluster=cluster, username=user.username))


def pick_port(cluster):
    ports = list(settings.JUPYTER_PORTS)
    for j in Jupyter.objects.filter(cluster=cluster):
        if j.port in ports:
            ports.remove(j.port)
    if len(ports) == 0:
        raise Exception('All ports are used!')
    index = randint(0, len(ports) - 1)
    return ports[index]


def start_jupyter_server(user, jupyter):
    jupyter_cmd = 'jupyter notebook --ip=0.0.0.0 --port=' + str(jupyter.port) + ' --NotebookApp.token=' + jupyter.token + ' --no-browser'
    cmd = 'su - ' + user.username + ' -c "' + cmd + '"'
    proc = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.stdin.write(self.password)
    proc.stdin.flush()
    jupyter.pid = proc.pid
    jupyter.save()
    proc.communicate()


def stop_jupyter_server(user, jupyter):
    jupyter_cmd = 'jupyter notebook stop ' + str(jupyter.port)
    user.run_command(jupyter_cmd)
