from sqlalchemy.ext.declarative import declared_attr
from zope.interface import implementer
import sqlalchemy as sa

from keyloop.interfaces.identity import IIdentity, IIdentitySource


@implementer(IIdentity)
class Identity:

    __tablename__ = "user"

    @declared_attr
    def id(self):
        return sa.Column(sa.Integer, autoincrement=True, primary_key=True)

    @declared_attr
    def username(self):
        return sa.Column(sa.String, autoincrement=True, primary_key=True)

    @declared_attr
    def password(self):
        return sa.Column(sa.String, autoincrement=True, primary_key=True)


@implementer(IIdentitySource)
class IdentitySource:
    def __init__(self, session):
        self.session = session

    def get(self, username):
        return self.session.query.filter(Identity.username == username).one()

    def create(self, username, password, name=None, contacts=None):
        return Identity(
            username=username, password=password, name=name, contacts=contacts
        )
