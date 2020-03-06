class IdentityNotFound(Exception):
    """Raise an error if identity has not been found"""
    pass


class AuthenticationFailed(Exception):
    """Raise an error if an user pass a wrong password"""
    pass
