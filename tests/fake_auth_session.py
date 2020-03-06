import uuid

import arrow

from keyloop.api.v1.exceptions import IdentityNotFound, AuthenticationFailed


class FakeAuthSession:

    test_delete_called = False
    generated_uuid = uuid.uuid4()
    identity = {}

    def __init__(self, identity, active, ttl, start, id):
        self.uuid = id
        self.identity = identity
        self.identity_id = identity.id
        self.active = active
        self.ttl = ttl
        self.start = start

    @classmethod
    def test_reset(cls):
        cls.test_delete_called = False

    @classmethod
    def get_identity(cls, username):
        if not username:
            raise IdentityNotFound

        return cls(cls.identity, True, 600, arrow.utcnow().datetime, cls.generated_uuid)

    @classmethod
    def login(cls, username, password):
        from tests.fake_user import FakeUser
        cls.identity = FakeUser(username='test@test.com.br', password='1234567a')
        cls.identity.uuid = uuid.uuid4()

        if username != cls.identity.username:
            raise IdentityNotFound

        if password != cls.identity.password:
            raise AuthenticationFailed

        return cls(cls.identity, True, 600, arrow.utcnow().datetime, cls.generated_uuid)
