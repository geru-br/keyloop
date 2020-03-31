class KeyloopError(Exception):
    """Base Exception."""
    pass


class IdentityNotFound(KeyloopError):
    """Raise an error if identity has not been found"""
    pass


class IdentityAlreadyExists(KeyloopError):
    """Raise an error if identity already exists"""
    pass


class AuthenticationFailed(KeyloopError):
    """Raise an error if an user pass a wrong password"""
    pass


class PermissionError(KeyloopError):
    """Base Exception for permission errors."""
    pass


class PermissionNotFound(PermissionError):
    """Permission not found."""
    pass


class PermissionAlreadyExists(PermissionError):
    """Permission already exists with specific name."""
    pass


class PermissionAlreadyGranted(PermissionError):
    """Permission-Identity association already exists."""
    pass
