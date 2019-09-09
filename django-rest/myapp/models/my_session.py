import random
import string
from django.db import models
from django.utils import timezone


def random_string_digits(stringLength=6):
    """Generate a random string of letters and digits """
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(stringLength))


class MySession(models.Model):
    uid = models.CharField(max_length=128)
    session_token = models.CharField(max_length=256)
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
        session.session_token = random_string_digits(128)
        session.active_at = timezone.now()
        session.save()
        return session
