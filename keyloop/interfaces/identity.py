import typing as T

from zope.interface import (
    Interface,
    Attribute
)


class IContact(Interface):
    type = Attribute('String to indicate type of contact (e.g. email, phone, etc...)')
    value = Attribute('String value of contact type')
    valid_for_auth = Attribute('Boolean to indicate if contact type is valid for auth')


class IIdentity(Interface):
    username = Attribute('Unique string used for identifying a user party.')
    password = Attribute('The password for verifying the user')
    active = Attribute('The indicator if the identity is active')


class IIdentitySource(Interface):
    """Marker interface for callables that retrieve an Identity object given a username
    """

    def get(identity_id: str) -> IIdentity:
        pass

    def create(username: str, password: str, name: T.Optional[str], contacts: T.Optional[T.List[IContact]]):
        pass

    def delete(identity_id: str):
        pass

    def update(identity_id: str, params: dict):
        pass
