import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy_utils import UUIDType
from zope.interface import implementer

from keyloop.api.v1.exceptions import PermissionAlreadyExists, PermissionNotFound
from keyloop.ext.utils.decorators import singleton, singletonmethod
from keyloop.interfaces.permission import IPermission, IPermissionSource
from keyloop.utils import generate_uuid


# @implementer(IPermissionGrantSource)
# @singleton
# class PermissionGrantSource:
#
#     def __init__(self, session, model):
#         self.model = model
#         self.session = session
#
#     def grant_permission(cls, permission_id, identity_id):
#         perm_ident_assoc = (permission_id, identity_id)
#         if perm_ident_assoc in cls.PERM_IDENT_ASSOCIATIONS:
#             raise PermissionGrantAlreadyExists
#
#         permission_grant = cls(*perm_ident_assoc)
#         cls.PERMISSION_GRANTS.update({permission_grant.uuid: permission_grant.__dict__})
#         cls.PERM_IDENT_ASSOCIATIONS.add(perm_ident_assoc)
#         return permission_grant


# @implementer(IPermissionGrant)
# class PermissionGrant:
#     __tablename__ = 'permission_grant'
#
#     @declared_attr
#     def id(self):
#         return sa.Column(sa.Integer, autoincrement=True, primary_key=True)
#
#     @declared_attr
#     def identity_id(self):
#         return sa.Column('identity_id', sa.Integer, sa.ForeignKey('identity.id'))
#
#     @declared_attr
#     def permission_id(self):
#         return sa.Column('permission_id', sa.Integer, sa.ForeignKey('permission.id'))


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
    def get_by(self, **kwargs):
        if 'name' in kwargs.keys():
            try:
                return self.session.query(self.model).filter_by(name=kwargs['name']).one()
            except NoResultFound:
                raise PermissionNotFound()
        elif 'uuid' in kwargs.keys():
            try:
                return self.session.query(self.model).filter_by(uuid=kwargs['uuid']).one()
            except NoResultFound:
                raise PermissionNotFound()

    @singletonmethod
    def create(self, name, description):
        permission = self.model(name=name, description=description)
        self.session.add(permission)

        try:
            self.session.flush()
        except IntegrityError:
            raise PermissionAlreadyExists()

        return permission
