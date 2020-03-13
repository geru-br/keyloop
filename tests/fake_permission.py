from keyloop.api.v1.exceptions import PermissionAlreadyExists, PermissionAlreadyGranted, PermissionNotFound
from keyloop.utils import generate_uuid


class FakePermission:
    PERMISSIONS = {}

    def __init__(self, name, description, uuid=None):
        self.uuid = uuid if uuid else generate_uuid()
        self.name = name
        self.description = description

    @classmethod
    def test_reset(cls):
        cls.PERMISSIONS = {}

    @classmethod
    def _get_by_name(cls, name):
        for perm in cls.PERMISSIONS.values():
            if perm['name'] == name:
                return cls(**perm)

        raise PermissionNotFound()

    @classmethod
    def get_by(cls, **kwargs):
        if 'name' in kwargs.keys():
            return cls._get_by_name(kwargs['name'])
        elif 'uuid' in kwargs.keys():
            params = cls.PERMISSIONS.get(kwargs['uuid'])
            if not params:
                raise PermissionNotFound()
            return cls(**params)

    @classmethod
    def create(cls, name, description):
        try:
            cls.get_by(name=name)
        except PermissionNotFound:
            permission = cls(name, description)
            cls.PERMISSIONS.update({permission.uuid: permission.__dict__})
            return permission
        else:
            raise PermissionAlreadyExists


class FakePermissionGrant:
    PERMISSION_GRANTS = {}
    PERM_IDENT_ASSOCIATIONS = set()

    def __init__(self, permission_id, identity_id):
        self.uuid = generate_uuid()
        self.permission_id = permission_id
        self.identity_id = identity_id

    @classmethod
    def test_reset(cls):
        cls.PERMISSION_GRANTS = {}
        cls.PERM_IDENT_ASSOCIATIONS = set()

    @classmethod
    def get(cls, uuid):
        return cls.PERMISSION_GRANTS.get(uuid)

    @classmethod
    def grant_permission(cls, permission_id, identity_id):
        perm_ident_assoc = (permission_id, identity_id)
        if perm_ident_assoc in cls.PERM_IDENT_ASSOCIATIONS:
            raise PermissionAlreadyGranted

        permission_grant = cls(*perm_ident_assoc)
        cls.PERMISSION_GRANTS.update({permission_grant.uuid: permission_grant.__dict__})
        cls.PERM_IDENT_ASSOCIATIONS.add(perm_ident_assoc)
        return permission_grant
