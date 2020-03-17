import arrow

from keyloop.api.v1.exceptions import IdentityNotFound, AuthenticationFailed
from keyloop.utils import generate_uuid


class FakeAuthSession:
    test_delete_called = False
    identity = None

    def __init__(self, identity, active, ttl, start, uuid=None):
        self.uuid = uuid if uuid else generate_uuid()
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

        return cls(cls.identity, True, 600, arrow.utcnow().datetime)

    @classmethod
    def login(cls, username, password):
        from tests.fake_user import FakeUser
        cls.identity = FakeUser.get(username=username)

        if not cls.identity:
            raise IdentityNotFound

        if password != cls.identity.password:
            raise AuthenticationFailed

        return cls(cls.identity, True, 600, arrow.utcnow().datetime)
