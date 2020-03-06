from keyloop.utils import generate_uuid


class FakePermission:
    PERMISSIONS = {}

    def __init__(self, name, description):
        self.uuid = generate_uuid()
        self.name = name
        self.description = description

    @classmethod
    def test_reset(cls):
        cls.PERMISSIONS = {}

    @classmethod
    def create(cls, name, description):
        permission = cls(name, description)
        cls.PERMISSIONS.update({permission.uuid: permission.__dict__})
        return permission
