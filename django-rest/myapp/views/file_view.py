import os
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models.my_file import MyFile
from . import check_session


@api_view(['GET'])
def get_directory(request, path):
    user = check_session(request)
    directory = MyFile(user, path, 'directory')
    return Response(directory.json())

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

@api_view(['POST'])
def delete_file_directory(request):
    user = check_session(request)
    path = request.data['path']
    name = request.data['name']
    MyFile.delete(user, os.path.join(path, name))
    parent = MyFile(user, path, 'directory')
    return Response(parent.json())

@api_view(['POST'])
def upload_file(request, path):
    user = check_session(request)
    file = request.FILES['file']
    MyFile.upload_file(user, path, file)
    parent = MyFile(user, path, 'directory')
    return Response(parent.json())

@api_view(['POST'])
def update_text(request, path):
    user = check_session(request)
    text = request.data['text']
    MyFile.update_text(user, path, text)
    file = MyFile(user, path, 'text file')
    return Response(file.json())

@api_view(['GET'])
def get_download_link(request, path):
    user = check_session(request)
    link = MyFile.get_download_link(user, path)
    return Response({'link': link})

@api_view(['POST'])
def paste_file_directory(request):
    user = check_session(request)
    src = request.data['src']
    dest = request.data['dest']
    MyFile.copy_paste(user, src, dest)
    dest = MyFile(user, dest, 'directory')
    return Response(dest.json())
