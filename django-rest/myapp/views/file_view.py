from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models.my_file import MyFile
from . import check_session


@api_view(['GET'])
def get_file(request, path):
    user = check_session(request)
    file = MyFile(user, path)
    return Response(file.json())

@api_view(['POST'])
def create_file(request):
    user = check_session(request)
    filename = request.data['filename']
    path = request.data['path']
    directory = MyFile.create_file(user, path, filename)
    return Response(directory.json())

@api_view(['POST'])
def create_directory(request):
    user = check_session(request)
    dirname = request.data['dirname']
    path = request.data['path']
    directory = MyFile.create_directory(user, path, dirname)
    return Response(directory.json())
