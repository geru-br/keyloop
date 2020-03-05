import uuid

import arrow


class FakeAuthSession:

    test_delete_called = False
    generated_uuid = uuid.uuid4()

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
    def get(cls, session_id):
        from tests.fake_user import FakeUser
        identity = FakeUser(username='teste@fakeauthsession.com', password='1234567a')
        identity.uuid = session_id
        return cls(identity, True, 600, arrow.utcnow().datetime, cls.generated_uuid)

    @classmethod
    def create(cls, identity, active, ttl, start):
        return cls(identity, active, ttl, start, cls.generated_uuid)

    @classmethod
    def delete(cls):
        cls.test_delete_called = True
        cls.active = False
