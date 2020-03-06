from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)
from zope.sqlalchemy import register

from keyloop.ext.sqla.identity import Identity
from keyloop.ext.sqla.permission import Permission

DBSession = scoped_session(sessionmaker())
register(DBSession)
Base = declarative_base()


class RealIdentity(Identity, Base):
    pass


class RealPermission(Permission, Base):
    pass

