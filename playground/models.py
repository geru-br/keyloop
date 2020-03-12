import sqlalchemy  as sa
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship)
from sqlalchemy_utils import UUIDType
from zope.sqlalchemy import register

from keyloop.ext.sqla.identity import Identity
from keyloop.ext.sqla.permission import Permission

DBSession = scoped_session(sessionmaker())
register(DBSession)
Base = declarative_base()

permission_grant_table = sa.Table(
    'permission_grant', Base.metadata,
    sa.Column('identity_id', UUIDType, sa.ForeignKey('identity.id')),
    sa.Column('permission_id', sa.Integer, sa.ForeignKey('permission.id'))
)


class RealIdentity(Identity, Base):
    @declared_attr
    def permissions(self):
        return relationship("RealPermission", secondary=permission_grant_table)


class RealPermission(Permission, Base):
    pass
