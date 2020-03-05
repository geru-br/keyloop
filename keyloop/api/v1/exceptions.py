class IdentityNotFound(Exception):
    """Raise an error if identity has not been found"""
    pass

class AuthSessionForbidden(Exception):
    """Raise an error if an user pass a wrong username or password"""
    pass
