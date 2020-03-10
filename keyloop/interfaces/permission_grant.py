from zope.interface import Attribute, Interface


class IPermissionGrant(Interface):
    permission_id = Attribute('FK for Permission model.')
    identity_id = Attribute('FK for Identity model')


class IPermissionGrantSource(Interface):
    """Marker interface for callables that retrieve a PermissionGrant object given a uuid
    """

    def get(uuid: str) -> IPermissionGrant:
        pass

    def create(self, permission_id: str, identity_id: str):
        pass
