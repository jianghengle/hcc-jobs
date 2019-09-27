from django.db import models
from django.utils import timezone
from .helpers import random_string_digits


class MySession(models.Model):
    uid = models.CharField(max_length=128)
    session_token = models.CharField(db_index=True, max_length=256)
    active_at = models.DateTimeField('last active at')

    def json(self):
        return {
            'uid': self.uid,
            'token': self.session_token
        }

    @staticmethod
    def create(uid):
        session = MySession()
        session.uid = uid
        session.session_token = random_string_digits(64)
        session.active_at = timezone.now()
        session.save()
        return session

    @staticmethod
    def get_by_token(token):
        return MySession.objects.get(session_token=token)
