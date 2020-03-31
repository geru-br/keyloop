from keyloop.api.v1.exceptions import IdentityNotFound, AuthenticationFailed, PermissionAlreadyGranted
from keyloop.utils import generate_uuid


class FakeUser:
    IDENTITIES = {}
    PERMISSION_GRANTS = set()  # Set of tuples (permission_uuid, identity_id)

    test_delete_result = True
    test_delete_called = False

    def __init__(self, username, password, name, active=True, uuid=None, permissions=[]):
        self.uuid = uuid if uuid else generate_uuid()
        self.username = username
        self.password = password
        self.name = name
        self.active = active
        self.permissions = permissions if permissions else ['perm_a', 'perm_b', 'perm_c']

    @classmethod
    def test_reset(cls):
        cls.IDENTITIES = {}
        cls.PERMISSION_GRANTS = set()

    @classmethod
    def _get_by_username(cls, username):
        for params in cls.IDENTITIES.values():
            if params['username'] == username:
                return cls(**params)

        raise IdentityNotFound()

    @classmethod
    def get(cls, uuid=None, username=None):
        if username:
            return cls._get_by_username(username)
        elif uuid:
            params = cls.IDENTITIES.get(str(uuid))
            if not params:
                raise IdentityNotFound()
            return cls(**params)

    @classmethod
    def create(cls, username, password, name=None):
        identity = cls(username, password, name, True)
        cls.IDENTITIES.update({str(identity.uuid): identity.__dict__})
        return identity

    @classmethod
    def delete(cls, identity):
        if not cls.IDENTITIES.get(str(identity.uuid)):
            raise IdentityNotFound()

        cls.IDENTITIES[str(identity.uuid)]['active'] = False

    @classmethod
    def update(cls, identity, params):
        for key, value in params.items():
            if key in ['username', 'password']:  # Does not update
                continue

            setattr(identity, key, value)

        cls.IDENTITIES.update({str(identity.uuid): identity.__dict__})

    @classmethod
    def change_password(cls, identity, last_password, password):
        if identity.password != last_password:
            raise AuthenticationFailed()

        identity.password = password
        cls.IDENTITIES.update({str(identity.uuid): identity.__dict__})

    @classmethod
    def grant_permission(cls, permission, identity):
        perm_grant = (str(permission.uuid), str(identity.uuid))
        if perm_grant in cls.PERMISSION_GRANTS:
            raise PermissionAlreadyGranted()

        cls.PERMISSION_GRANTS.add(perm_grant)
