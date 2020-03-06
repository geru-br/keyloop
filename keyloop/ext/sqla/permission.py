import sqlalchemy as sa
import transaction
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy_utils import UUIDType
from zope.interface import implementer

from keyloop.ext.utils.decorators import singleton, singletonmethod
from keyloop.interfaces.permission import IPermission, IPermissionSource
from keyloop.utils import generate_uuid


class IdentityPermissionAssociation:
    __tablename__ = 'identity_permission_association'

    @declared_attr
    def id(self):
        return sa.Column(sa.Integer, autoincrement=True, primary_key=True)

    @declared_attr
    def identity_id(self):
        return sa.Column('identity_id', sa.Integer, sa.ForeignKey('identity.id'))

    @declared_attr
    def permission_id(self):
        return sa.Column('permission_id', sa.Integer, sa.ForeignKey('permission.id'))


@implementer(IPermission)
@singleton
class Permission:
    __tablename__ = 'permission'

    @declared_attr
    def id(self):
        return sa.Column(sa.Integer, autoincrement=True, primary_key=True)

    @declared_attr
    def uuid(self):
        return sa.Column(UUIDType, default=generate_uuid)

    @declared_attr
    def name(self):
        return sa.Column(sa.String, unique=True, index=True)

    @declared_attr
    def description(self):
        return sa.Column(sa.String, nullable=False)


@implementer(IPermissionSource)
@singleton
class PermissionSource:
    def __init__(self, session, model):
        self.model = model
        self.session = session

    @singletonmethod
    def get(self, name):
        return self.session.query(self.model).filter_by(name=name).one()

    @singletonmethod
    def create(self, name, description):
        permission = self.model(name=name, description=description)
        self.session.add(permission)

        transaction.commit()
        return self.get(name)
