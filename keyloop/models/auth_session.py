class AuthSession:
    def __init__(self, username, password, identity=None):
        self.username = username
        self.password = password
        self.identity = identity
