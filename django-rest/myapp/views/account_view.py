from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models import MySession
from ..models.my_user import MyUser

@api_view(['Post'])
def login_user(request):
    username = request.data['username']
    password = request.data['password']
    try:
        user = MyUser(username)
        user.verify_password(password)
        session = MySession.create(username)
        return Response({'user': user.json(), 'session': session.json()})
    except:
        return Response({'user': None})

