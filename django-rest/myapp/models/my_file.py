import os
import shutil
from django.conf import settings
from .helpers import random_string_digits


class MyFile(object):
    def __init__(self, user, path, file_type=None):
        self.user = user
        self.path = path
        self.name = os.path.basename(path)
        self.type = file_type
        self.content = None

        if not file_type:
            self.get_type()

        self.get_content()

    def get_type(self):
        file_cmd = 'file -b ' + '"' + self.path + '"'
        file_result = self.user.run_command(file_cmd)
        if file_result == 'cannot open (No such file or directory)':
            raise Exception('no such file')

        if 'no read permission' in file_result:
            raise Exception('permission denied')
        elif file_result == 'empty':
            self.type = 'text file'
        elif file_result == 'very short file (no magic)':
            self.type = 'text file'
        elif file_result == 'directory':
            self.type = 'directory'
        elif file_result.startswith('symbolic link to'):
            self.type = 'symbolic link'
            self.content = file_result
        elif 'ASCII text' in file_result or 'UTF-8 Unicode text' in file_result:
            self.type = 'text file'
        else:
            self.type = 'binary file'

    def get_content(self):
        if self.type == 'directory':
            ls_cmd = 'ls -lhoQ ' + '"' + self.path + '"'
            self.content = self.user.run_command(ls_cmd)
        elif self.type == 'text file':
            cat_cmd = 'cat ' + '"' + self.path + '"'
            self.content = self.user.run_command(cat_cmd)

    def json(self):
        return {
            'path': self.path,
            'name': self.name,
            'type': self.type,
            'content': self.content
        }

    @staticmethod
    def create_file(user, path, filename):
        full_path = os.path.join(path, filename)
        touch_cmd = 'touch ' + '"' + full_path + '"'
        user.run_command(touch_cmd)

    @staticmethod
    def create_directory(user, path, dirname):
        full_path = os.path.join(path, dirname)
        mkdir_cmd = 'mkdir ' + '"' + full_path + '"'
        user.run_command(mkdir_cmd)

    @staticmethod
    def update_name(user, path, old_name, new_name):
        old_full_path = os.path.join(path, old_name)
        new_full_path = os.path.join(path, new_name)
        mv_cmd = 'mv -n -T ' + '"' + old_full_path + '" "' + new_full_path + '"'
        user.run_command(mv_cmd)

    @staticmethod
    def delete(user, full_path):
        rm_cmd = 'rm -r ' + '"' + full_path + '"'
        user.run_command(rm_cmd)

    @staticmethod
    def upload_file(user, path, file):
        filename = file.name
        temp_dir = settings.TEMP_DIR
        temp_string = random_string_digits(32)
        os.makedirs(os.path.join(temp_dir, temp_string))
        temp_file_path = os.path.join(temp_dir, temp_string, filename)
        with open(temp_file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        copy_file(user, temp_file_path, path + '/')
        shutil.rmtree(os.path.join(temp_dir, temp_string))

    @staticmethod
    def update_text(user, path, text):
        temp_dir = settings.TEMP_DIR
        temp_string = random_string_digits(32)
        temp_file_path = os.path.join(temp_dir, temp_string)
        f= open(temp_file_path, 'w+')
        f.write(text)
        f.close()
        copy_file(user, temp_file_path, path)
        os.remove(temp_file_path)

    @staticmethod
    def get_download_link(user, path):
        temp_dir = settings.TEMP_DIR
        temp_string = random_string_digits(32)
        temp_path = os.path.join(temp_dir, temp_string)
        os.makedirs(temp_path)
        os.chmod(temp_path, 0o777)
        copy_file(user, path, temp_path, False)
        filename = os.path.basename(path)
        return '/static/tmp/' +  temp_string + '/' + filename

    @staticmethod
    def copy_paste(user, src, dest):
        copy_file(user, src, dest + '/')


def copy_file(user, src, dest, recursive=True):
    if recursive:
        cp_cmd = 'cp -r ' + '"' + src + '"' + ' "' + dest + '"'
    else:
        cp_cmd = 'cp ' + '"' + src + '"' + ' "' + dest + '"'
    user.run_command(cp_cmd)
