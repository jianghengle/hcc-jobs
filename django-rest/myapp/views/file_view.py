from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models.my_file import MyFile
from . import check_session


@api_view(['GET'])
def get_file(request, path):
    user = check_session(request)
    file = MyFile(user, path)
    return Response(file.json())

