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

    def login(username, password) -> bool:
        """Verify the identity."""
        pass


class IIdentitySource(Interface):
    """Marker interface for callables that retrieve an Identity object given a username
    """

    def get(identity_id) -> IIdentity:
        pass

    def create(username: str, password: str, name: T.Optional[str], contacts: T.Optional[T.List[IContact]]):
        pass

    def delete(id: str):
        pass
