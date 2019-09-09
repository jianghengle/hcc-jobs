from django.db import models


class MySession(models.Model):
    uid = models.CharField(max_length=128)
    session_token = models.CharField(max_length=256)
    active_at = models.DateTimeField('last active at')
