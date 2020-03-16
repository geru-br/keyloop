import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy_pagination import paginate
from sqlalchemy_utils import UUIDType
from zope.interface import implementer

from keyloop.api.v1.exceptions import PermissionAlreadyExists, PermissionNotFound
from keyloop.ext.utils.decorators import singleton, singletonmethod
from keyloop.interfaces.permission import IPermission, IPermissionSource
from keyloop.utils import generate_uuid


@implementer(IPermission)
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
    def get(self, uuid=None, name=None):
        if name:
            query = self.session.query(self.model).filter_by(name=name)
        elif uuid:
            query = self.session.query(self.model).filter_by(uuid=uuid)
        else:
            return

        try:
            return query.one()
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

    @singletonmethod
    def list(self, page, limit):
        permissions = paginate(self.session.query(self.model), page, limit)
        params = {
            'items': permissions.items,
            'document_meta': {
                'prev': permissions.previous_page,
                'next': permissions.next_page,
                'page': permissions.pages,
                'total': permissions.total
            }
        }
        return params
