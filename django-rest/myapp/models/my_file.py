import os


class MyFile(object):
    def __init__(self, user, path):
        self.user = user
        self.path = path
        self.name = os.path.basename(path)

        file_cmd = 'file -b ' + '\'' + path + '\''
        file_result = user.run_command(file_cmd)
        if file_result == 'cannot open (No such file or directory)':
            raise Exception('no such file')

        if 'no read permission' in file_result:
            raise Exception('permission denied')
        elif file_result == 'empty':
            self.type = 'text file'
            self.content = ''
        elif file_result == 'very short file (no magic)':
            self.type = 'text file'
            self.content = ''
        elif file_result == 'directory':
            self.type = 'directory'
            ls_cmd = 'ls -lhoQ ' + '\'' + path + '\''
            self.content = user.run_command(ls_cmd)
        elif file_result.startswith('symbolic link to'):
            self.type = 'symbolic link'
            self.content = file_result
        elif 'ASCII text' in file_result:
            self.type = 'text file'
            cat_cmd = 'cat ' + '\'' + path + '\''
            self.content = user.run_command(cat_cmd)
        else:
            self.type = 'binary file'
            self.content = None

    def json(self):
        return {
            'path': self.path,
            'name': self.name,
            'type': self.type,
            'content': self.content
        }
