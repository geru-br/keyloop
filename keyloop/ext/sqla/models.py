from sqlalchemy.ext.declarative import declared_attr
from zope.interface import implementer
import sqlalchemy as sa

from keyloop.ext.utils.decorators import singleton, singletonmethod
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
@singleton
class IdentitySource:
    model = None
    session = None

    def __init__(self, session, model):
        self.model = model
        self.session = session

    @singletonmethod
    def get(self, username):
        return self.session.query(self.model).filter(self.model.username == username).one()

    @singletonmethod
    def create(self, username, password, name=None, contacts=None):
        return self.model(
            username=username, password=password, name=name, contacts=contacts
        )
