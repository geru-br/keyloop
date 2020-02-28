from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)
from zope.sqlalchemy import register

from keyloop.ext.sqla.auth_session import AuthSession
from keyloop.ext.sqla.models import Identity, Contact

DBSession = scoped_session(sessionmaker())
register(DBSession)
Base = declarative_base()


class RealIdentity(Identity, Base):

    def login(self, username, password):
        return self.username == username and self.password == password


class RealContact(Contact, Base):
    pass


class RealAuthSesion(AuthSession, Base):

    def delete(self):
        self.active=False
