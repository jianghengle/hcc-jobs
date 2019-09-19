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

        if file_result == 'directory':
            self.type = 'directory'
            ls_cmd = 'ls -AlhoQ ' + '\'' + path + '\''
            self.content = user.run_command(ls_cmd)
        elif file_result.startswith('symbolic link to'):
            self.type = 'symbolic link'
            self.content = file_result
        elif file_result == 'ASCII text':
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
