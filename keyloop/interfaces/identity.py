import typing as T

from zope.interface import (
    Interface,
    Attribute
)


class IIdentity(Interface):
    username = Attribute('Unique string used for identifying a user party.')
    password = Attribute('The password for verifying the user')
    active = Attribute('The indicator if the identity is active')


class IIdentitySource(Interface):
    """Marker interface for callables that retrieve an Identity object given a username
    """

    def get(identity_id: str) -> IIdentity:
        pass

    def change_password(identity_id: str, last_password: str, password: str):
        pass

    def create(username: str, password: str, name: T.Optional[str]):
        pass

    def delete(identity_id: str):
        pass

    def update(identity_id: str, params: dict):
        pass

    def grant_permission(permission, identity):
        pass
