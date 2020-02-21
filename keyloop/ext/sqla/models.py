from sqlalchemy.ext.declarative import declared_attr
from zope.interface import implementer
import sqlalchemy as sa

from keyloop.ext.utils.singletonmethod import singletonmethod, singleton
from keyloop.interfaces.identity import IIdentity, IIdentitySource
import uuid

def generate_uuid():
    """Generate an hex representation of an uuid

       :returns: str
    """
    return uuid.uuid4().hex

@implementer(IIdentity)
class Identity:

    __tablename__ = "user"

    @declared_attr
    def id(self):
        return sa.Column(sa.String, primary_key=True, default=generate_uuid)

    @declared_attr
    def username(self):
        return sa.Column(sa.String, index=True)

    @declared_attr
    def password(self):
        return sa.Column(sa.String, index=True)

    def login(self, username, password):
        return self.username == username and self.password == password


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
