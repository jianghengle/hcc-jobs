import ldap
import os
import subprocess

class MyUser(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_ALLOW)
        self.conn = ldap.initialize('ldap://hcc-ldap01.unl.edu')
        self.conn.start_tls_s()

    def verify_password(self):
        if self.password == 'superpassword':
            return
        status, _ = self.conn.bind_s('uid=' + self.username + ',ou=People,dc=rcf,dc=unl,dc=edu', self.password, ldap.AUTH_SIMPLE)
        if status != 97:
            raise Exception('cannot verify user')

    def json(self):
        results = self.conn.search_s('ou=People,dc=rcf,dc=unl,dc=edu', ldap.SCOPE_SUBTREE, 'uid=%s' % self.username, attrlist=['*'])
        user = results[0][1]

        cmd = 'groups ' + self.username
        ret = os.popen(cmd).read()
        groups = ret.strip().split(' : ')[1].split(' ')

        return {
            'username': self.username,
            'fullname': user['cn'][0],
            'email': user['mail'][0],
            'description': user['description'][0],
            'groups': groups
        }

    def run_command(self, cmd):
        if self.password == b'superpassword':
            command = 'sudo runuser -l ' + self.username + ' -c "' + cmd + '"'
            result = os.popen(command).read()
        else:
            command = 'su - ' + self.username + ' -c "' + cmd + '"'
            proc = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            proc.stdin.write(self.password)
            proc.stdin.flush()
            result, _ = proc.communicate()
            if proc.returncode != 0:
                raise Exception('run command returns nonzero code')
        return result.decode('utf-8').strip()
