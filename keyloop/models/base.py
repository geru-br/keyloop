import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)

from uuid import uuid4
from zope.sqlalchemy import register

__all__ = [
    "DBSession",
]


DBSession = scoped_session(sessionmaker())
register(DBSession)


class CustomBase:
    query = DBSession.query_property()
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    uuid = sa.Column(
        sa.String(32),
        nullable=False,
        unique=True,
        index=True,
        default=lambda: uuid4().hex,
    )


Base = declarative_base(cls=CustomBase)
