from keyloop.api.v1.exceptions import IdentityNotFound, AuthenticationFailed, PermissionAlreadyGranted
from keyloop.utils import generate_uuid


class FakeUser:
    IDENTITIES = {}
    PERMISSION_GRANTS = set()  # Set of tuples (permission_uuid, identity_id)

    test_delete_result = True
    test_delete_called = False

    def __init__(self, username, password, active=True, name=None, id=None, permissions=[]):
        self.id = id if id else generate_uuid()
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
    def get_by(cls, **kwargs):
        if 'username' in kwargs.keys():
            return cls._get_by_username(kwargs['username'])
        elif 'uuid' in kwargs.keys():
            params = cls.IDENTITIES.get(str(kwargs['uuid']))
            if not params:
                raise IdentityNotFound()
            return cls(**params)

    @classmethod
    def create(cls, username, password, name=None, contacts=None):
        identity = cls(username, password, True, name, contacts)
        cls.IDENTITIES.update({str(identity.id): identity.__dict__})
        return identity

    @classmethod
    def delete(cls, identity_id):
        if not cls.IDENTITIES.get(str(identity_id)):
            raise IdentityNotFound()

        cls.IDENTITIES[str(identity_id)]['active'] = False

    @classmethod
    def update(cls, identity_id, params):
        identity = cls.IDENTITIES.get(str(identity_id))
        if not identity:
            raise IdentityNotFound()

        identity['name'] = params['name']

    @classmethod
    def change_password(cls, identity_id, last_password, password):
        identity = cls.IDENTITIES.get(str(identity_id))
        if not identity:
            raise IdentityNotFound()

        if identity['password'] != last_password:
            raise AuthenticationFailed()

        identity['password'] = password

    @classmethod
    def grant_permission(cls, permission, identity):
        perm_grant = (str(permission.uuid), str(identity.id))
        if perm_grant in cls.PERMISSION_GRANTS:
            raise PermissionAlreadyGranted()

        cls.PERMISSION_GRANTS.add(perm_grant)
