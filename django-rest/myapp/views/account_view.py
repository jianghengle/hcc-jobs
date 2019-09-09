from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models import MySession
from ..models.my_user import MyUser

@api_view(['Post'])
def verify_user(request):
    username = request.data['username']
    password = request.data['password']
    try:
        user = MyUser(username, password)
        return Response(user.to_json())
    except:
        return Response({'ok': False})

