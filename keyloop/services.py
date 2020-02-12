class AuthenticationService(object):
    def __init__(self, backend):
        self.backend = backend

    def login(self, login, password):
        """
        Authenticates the user by their login property and password.
        Will raise an `AuthenticationException` if the username or password
        are not found.
        """
        #TODO: Check if the user is activated?
        #TODO: Add a database log of authentication attempts
        #TODO: Prevent multiple attempts from same IP
        user = self.backend.get_user(login)

        if (
            user is None or
            validacao
        ):
            print('Error')

        return user


def test_authenticate_good_user(self):

        def get_user(login):
            if login == 'sontek':
                return self._make_user(login, 'drowssap')
            else:
                return None

        s = mock.Mock()
        s.get_user = get_user
        f = AuthenticationService(s)

        result = f.login('sontek', 'drowssap')

        assert result is not None
