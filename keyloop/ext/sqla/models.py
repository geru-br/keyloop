from sqlalchemy.ext.declarative import declared_attr
from zope.interface import implementer
import sqlalchemy as sa

from keyloop.ext.utils.singletonmethod import singletonmethod, singleton
from keyloop.interfaces.identity import IIdentity, IIdentitySource


@implementer(IIdentity)
class Identity:

    __tablename__ = "user"

    @declared_attr
    def id(self):
        return sa.Column(sa.Integer, autoincrement=True, primary_key=True)

    @declared_attr
    def username(self):
        return sa.Column(sa.String, index=True)

    @declared_attr
    def password(self):
        return sa.Column(sa.String, index=True)


@implementer(IIdentitySource)
class IdentitySource:
    model = None
    session = None

    # def __init__(self, session, model):
    #     self.model = model
    #     self.session = session

    @classmethod
    def get(cls, username):
        from playground.models import RealIdentity

        return cls.session.query(cls.model).filter(cls.model.username == username).one()

    @classmethod
    def create(cls, username, password, name=None, contacts=None):
        return cls.model(
            username=username, password=password, name=name, contacts=contacts
        )
