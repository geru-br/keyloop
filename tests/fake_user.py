from keyloop.api.v1.exceptions import IdentityNotFound, AuthenticationFailed


class FakeUser:
    IDENTITIES = {}

    def __init__(self, username, password, active=True, name=None):
        self.id = '1bed6e99-74d8-484a-a650-fab8f4f80506'
        self.username = username
        self.password = password
        self.name = name
        self.active = active
        self.permissions = ['perm_a', 'perm_b', 'perm_c']

    @classmethod
    def test_reset(cls):
        cls.IDENTITIES = {}

    @classmethod
    def get(cls, uuid):
        identity = cls('test@test.com.br', password="1234567a")
        identity.uuid = uuid
        return identity

    @classmethod
    def create(cls, username, password, name):
        params = {
            'username': username,
            'password': password,
            'active': True,
            'name': name,
        }

        cls.IDENTITIES.update({'1bed6e99-74d8-484a-a650-fab8f4f80506': params})
        return cls(username, password, True, name)

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
