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
    MyFile.create_file(user, path, filename)
    parent = MyFile(user, path, 'directory')
    return Response(parent.json())

@api_view(['POST'])
def create_directory(request):
    user = check_session(request)
    dirname = request.data['dirname']
    path = request.data['path']
    MyFile.create_directory(user, path, dirname)
    parent = MyFile(user, path, 'directory')
    return Response(parent.json())

@api_view(['POST'])
def update_file_directory(request):
	user = check_session(request)
	path = request.data['path']
	old_name = request.data['oldName']
	new_name = request.data['newName']
	MyFile.update_name(user, path, old_name, new_name)
	parent = MyFile(user, path, 'directory')
	child = MyFile(user, os.path.join(path, new_name))
	return Response({'parent': parent.json(), 'child': child.json()})
