from keyloop.api.v1.exceptions import IdentityNotFound, AuthenticationFailed
from keyloop.utils import generate_uuid


class FakeUser:
    IDENTITIES = {}

    test_delete_result = True
    test_delete_called = False

    def __init__(self, username, password, active=True, name=None, contacts=None, id=None, permissions=None):
        # self.id = '1bed6e99-74d8-484a-a650-fab8f4f80506'
        self.id = id if id else generate_uuid()
        self.username = username
        self.password = password
        self.name = name
        self.active = active
        self.permissions = permissions if permissions else ['perm_a', 'perm_b', 'perm_c']

    @classmethod
    def test_reset(cls):
        cls.IDENTITIES = {}

    @classmethod
    def get(cls, uuid):
        params = cls.IDENTITIES.get(uuid)
        return cls(**params)

    @classmethod
    def create(cls, username, password, name, contacts):
        identity = cls(username, password, True, name, contacts)
        cls.IDENTITIES.update({identity.id: identity.__dict__})
        return identity

    def login(self, username, password):
        self.__class__.test_login_called = True
        return self.__class__.test_login_result

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
