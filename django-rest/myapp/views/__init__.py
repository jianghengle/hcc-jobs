import base64
from django.utils import timezone
from ..models import MySession
from ..models.my_user import MyUser


def check_session(request):
    token = request.META.get('HTTP_MYAUTHORIZATION')
    if not token:
        raise Exception('no token found')
    tp = token.split('$')
    session = MySession.get_by_token(tp[0])
    now = timezone.now()
    span = now - session.active_at
    if span.total_seconds() > 21600:
        raise Exception('token expired')
    session.active_at = now
    session.save()
    return MyUser(session.uid, base64.b64decode(tp[1]))
