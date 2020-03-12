from keyloop.api.v1.exceptions import PermissionAlreadyExists, PermissionNotFound
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

    @classmethod
    def list(cls, page, limit):
        params = []
        total = len(cls.PERMISSIONS) if limit > len(cls.PERMISSIONS) else limit
        current_page = 0 if page in (0, 1) else page

        if not cls.PERMISSIONS:
            return params

        params.append(list(cls.PERMISSIONS.items())[0][1])

        return params[current_page:total]

