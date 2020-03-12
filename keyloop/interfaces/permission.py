import typing as T

from zope.interface import Attribute, Interface


class IPermission(Interface):
    name = Attribute('Unique string used for identifying permission.')
    description = Attribute('Detailed information about the permission.')


class IPermissionSource(Interface):
    """Marker interface for callables that retrieve a Permission object given a name/uuid
    """

    def get_by(name: str, uuid: str) -> IPermission:
        pass

    def create(self, name: str, description: T.Optional[str]):
        pass
