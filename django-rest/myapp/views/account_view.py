from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models import MySession
from ..models.my_user import MyUser
from . import check_session

@api_view(['POST'])
def login_user(request):
    username = request.data['username']
    password = request.data['password']
    try:
        user = MyUser(username, password)
        user.verify_password()
        session = MySession.create(username)
        return Response({'user': user.json(), 'session': session.json()})
    except:
        return Response({'user': None})


@api_view(['GET'])
def get_user(request):
    user = check_session(request)
    return Response(user.json())


@api_view(['POST'])
def change_password(request):
    user = check_session(request)
    new_password = request.data['newPassword']
    result = user.change_password(new_password)
    if result == None:
        return Response({'ok': True})
    return Response({'ok': False, 'err': result})
