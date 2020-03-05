from keyloop.api.v1.exceptions import IdentityNotFound


class FakeUser:
    IDENTITIES = {}
    test_login_result = True
    test_login_called = False

    test_delete_result = True
    test_delete_called = False

    def __init__(self, username, password, name=None, contacts=None):
        self.id = '1bed6e99-74d8-484a-a650-fab8f4f80506'
        self.username = username
        self.password = password
        self.name = name
        self.contacts = contacts
        self.permissions = ['perm_a', 'perm_b', 'perm_c']

    @classmethod
    def test_reset(cls):
        cls.test_login_result = True
        cls.test_login_called = False
        cls.IDENTITIES = {}

    @classmethod
    def get(cls, uuid):
        identity = cls('test@test.com.br', password="1234567a")
        identity.uuid = uuid
        return identity

    @classmethod
    def create(cls, username, password, name, contacts):
        params = {
            'username': username,
            'password': password,
            'name': name,
            'contacts': contacts
        }

        cls.IDENTITIES.update({'1bed6e99-74d8-484a-a650-fab8f4f80506': params})
        return cls(username, password, name, contacts)

    def login(self, username, password):
        self.__class__.test_login_called = True
        return self.__class__.test_login_result

    @classmethod
    def delete(cls, id):
        if not cls.IDENTITIES.get(str(id)):
            raise IdentityNotFound()

        del cls.IDENTITIES[str(id)]

    @classmethod
    def update(cls, id, params):
        identity = cls.IDENTITIES.get(str(id))
        if not identity:
            raise IdentityNotFound()

        identity['name'] = params['name']
