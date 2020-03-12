class IdentityNotFound(Exception):
    """Raise an error if identity has not been found"""
    pass


class IdentityAlreadyExists(Exception):
    """Raise an error if identity already exists"""
    pass


class AuthenticationFailed(Exception):
    """Raise an error if an user pass a wrong password"""
    pass


class PermissionNotFound(Exception):
    """Permission not found."""
    pass


class PermissionAlreadyExists(Exception):
    """Permission already exists with specific name."""
    pass


class PermissionGrantAlreadyExists(Exception):
    """Permission-Identity association already exists."""
    pass
