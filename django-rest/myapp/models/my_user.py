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
        self.ldap_entry = None

    def verify_password(self):
        status, _ = self.conn.bind_s('uid=' + self.username + ',ou=People,dc=rcf,dc=unl,dc=edu', self.password, ldap.AUTH_SIMPLE)
        if status != 97:
            raise Exception('cannot verify user')

        self.get_ldap_entry()
        if 'nsAccountLock' in self.ldap_entry.keys() and self.ldap_entry['nsAccountLock'][0] == 'true':
            raise Exception('user has been locked')

    def get_ldap_entry(self):
        if self.ldap_entry == None:
            results = self.conn.search_s('ou=People,dc=rcf,dc=unl,dc=edu', ldap.SCOPE_SUBTREE, 'uid=%s' % self.username, attrlist=['*'])
            self.ldap_entry = results[0][1]

    def change_password(self, new_password):
        self.verify_password()
        result = None
        try:
            self.conn.passwd_s('uid=' + self.username + ',ou=People,dc=rcf,dc=unl,dc=edu', self.password, new_password)
        except Exception as e:
            result = str(e)
        return result

    def json(self):
        self.get_ldap_entry()

        cmd = 'groups ' + self.username
        ret = os.popen(cmd).read()
        groups = ret.strip().split(' : ')[1].split(' ')

        return {
            'username': self.username,
            'fullname': self.ldap_entry.get('cn', [''])[0],
            'email': self.ldap_entry.get('mail', [''])[0],
            'description': self.ldap_entry.get('description', [''])[0],
            'groups': groups
        }

    def run_command(self, cmd):
        command = 'su - ' + self.username + ' -c \'' + cmd + '\''
        proc = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.stdin.write(self.password)
        proc.stdin.flush()
        result, err = proc.communicate()
        if proc.returncode != 0:
            raise Exception('run command returns nonzero code: ' + str(proc.returncode) + '\nerr: ' + err.decode('utf-8'))
        return result.decode('utf-8').strip()
