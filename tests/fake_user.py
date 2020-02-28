from uuid import uuid4


class FakeUser:
    test_login_result = True
    test_login_called = False

    test_delete_result = True
    test_delete_called = False

    def __init__(self, username, password, name=None, contacts=None):
        self.id = 2
        self.uuid = uuid4().hex
        self.username = username
        self.password = password
        self.name = name
        self.contacts = contacts
        self.permissions = ['perm_a', 'perm_b', 'perm_c']

    @classmethod
    def test_reset(cls):
        cls.test_login_result = True
        cls.test_login_called = False

    @classmethod
    def get(cls, uuid):
        identity = cls('teste@email.com.br', password="1234567a")
        identity.uuid = uuid
        return identity

    @classmethod
    def create(cls, username, password, name, contacts):
        return cls(username, password, name, contacts)

    def login(self, username, password):
        self.__class__.test_login_called = True
        return self.__class__.test_login_result

    @classmethod
    def delete(cls, id):
        cls.test_delete_called = True
        return cls.test_delete_result
