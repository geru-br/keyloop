import datetime as DT

from sqlalchemy.ext.declarative import declared_attr
from zope.interface import implementer
import sqlalchemy as sa

from keyloop.interfaces.auth_session import IAuthSession, IAuthSessionSource
import uuid


@implementer(IAuthSession)
class AuthSession:

    __tablename__ = "auth_session"

    @declared_attr
    def id(self):
        return sa.Column(sa.String, primary_key=True, default=uuid.uuid4)

    @declared_attr
    def identity_id(cls):
        return sa.Column('identity_id', sa.ForeignKey('identity.id'))

    @declared_attr
    def identity(cls):
        return sa.orm.relationship("Identity")

    @declared_attr
    def active(self):
        return sa.Column(sa.Boolean, index=True)

    @declared_attr
    def ttl(self):
        return sa.Column(sa.Integer)

    @declared_attr
    def start(self):
        return sa.Column(sa.DateTime, index=True)

    def delete(self):
        self.active=False


@implementer(IAuthSessionSource)
class AuthSessionSource:
    model = None
    session = None

    @classmethod
    def get(cls, session_id):
        return cls.session.query(cls.model).filter(cls.model.id == session_id).one()

    @classmethod
    def create(cls, related_identity: str, ttl: int, start: DT.datetime):
        return cls.model(
            related_identity=related_identity, ttl=ttl, start=start
        )
