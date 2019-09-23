import os


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
        file_cmd = 'file -b ' + '\'' + self.path + '\''
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
        elif 'ASCII text' in file_result:
            self.type = 'text file'
        else:
            self.type = 'binary file'

    def get_content(self):
        if self.type == 'directory':
            ls_cmd = 'ls -lhoQ ' + '\'' + self.path + '\''
            self.content = self.user.run_command(ls_cmd)
        elif self.type == 'text file':
            cat_cmd = 'cat ' + '\'' + self.path + '\''
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
        touch_cmd = 'touch ' + '\'' + full_path + '\''
        user.run_command(touch_cmd)
        return MyFile(user, path, 'directory')

    @staticmethod
    def create_directory(user, path, dirname):
        full_path = os.path.join(path, dirname)
        mkdir_cmd = 'mkdir ' + '\'' + full_path + '\''
        user.run_command(mkdir_cmd)
        return MyFile(user, path, 'directory')
