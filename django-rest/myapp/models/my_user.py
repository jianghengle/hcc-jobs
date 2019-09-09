import ldap

class MyUser(object):
    def __init__(self, username, password):
        self.username = username
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_ALLOW)
        conn = ldap.initialize('ldap://hcc-ldap01.unl.edu')
        conn.start_tls_s()
        (status, ) = conn.bind_s('uid=' + username + ',ou=People,dc=rcf,dc=unl,dc=edu', password,  ldap.AUTH_SIMPLE)
        if status != 97:
        	raise 'cannot verify user'

    def json(self):
        return {
            "username": self.username
        }
