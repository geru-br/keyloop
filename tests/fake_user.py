class FakeUser:
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

    @classmethod
    def test_reset(cls):
        cls.test_login_result = True
        cls.test_login_called = False

    @classmethod
    def get(cls, username):
        return cls(username, password="1234567a")

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

