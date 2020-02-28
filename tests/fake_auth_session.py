import uuid

import arrow


class FakeAuthSession:

    def __init__(self, identity, active, ttl, start):
        self.id = uuid.uuid4()
        self.identity = identity
        self.identity_id = identity.id
        self.active = active
        self.ttl = ttl
        self.start = start

    @classmethod
    def get(cls, uuid):
        from tests.fake_user import FakeUser
        identity = FakeUser(username='teste@fakeauthsession.com', password='1234567a')
        identity.uuid = uuid
        return cls(identity, True, 600, arrow.utcnow().datetime)

    @classmethod
    def create(cls, identity, active, ttl, start):
        return cls(identity, active, ttl, start)

    def delete(self, uuid):
        pass
