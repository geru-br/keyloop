import cryptacular
import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy_utils.types.uuid import UUIDType
from zope.interface import implementer

from keyloop.api.v1.exceptions import IdentityNotFound, AuthenticationFailed, IdentityAlreadyExists, PermissionAlreadyGranted
from keyloop.ext.sqla.auth_session import password_check
from keyloop.ext.utils.decorators import singleton, singletonmethod
from keyloop.interfaces.identity import IIdentity, IIdentitySource
from keyloop.utils import generate_uuid

bcrypt = cryptacular.bcrypt.BCRYPTPasswordManager()


@implementer(IIdentity)
class Identity:
    __tablename__ = "identity"

    @declared_attr
    def id(self):
        return sa.Column(UUIDType, primary_key=True, default=generate_uuid)

    @declared_attr
    def username(self):
        return sa.Column(sa.String, index=True, unique=True)

    @declared_attr
    def password(self):
        return sa.Column(sa.String, nullable=False)

    @declared_attr
    def name(self):
        return sa.Column(sa.String)

    @declared_attr
    def active(self):
        return sa.Column(sa.Boolean, default=True)

    @declared_attr
    def permissions(self):
        raise NotImplemented()


@implementer(IIdentitySource)
@singleton
class IdentitySource:

    def __init__(self, session, model):
        self.model = model
        self.session = session

    @staticmethod
    def _set_password(value):
        return bcrypt.encode(value)

    @singletonmethod
    def get_by(self, **kwargs):
        active_users = self.session.query(self.model).filter(self.model.active == True)

        if 'username' in kwargs:
            query = active_users.filter_by(username=kwargs['username'])
        elif 'uuid' in kwargs:
            query = active_users.filter_by(id=kwargs['uuid'])
        else:
            return

        try:
            return query.one()
        except NoResultFound:
            raise IdentityNotFound()

    @singletonmethod
    def create(self, username, password, name=None):
        identity = self.model(username=username, password=self._set_password(password), name=name)
        self.session.add(identity)

        try:
            self.session.flush()

        except IntegrityError:
            raise IdentityAlreadyExists

        return identity

    @singletonmethod
    def delete(self, identity_id):
        identity = self.get(identity_id)

        identity.active = False

    @singletonmethod
    def update(self, identity_id, params):
        try:
            identity = self.session.query(self.model).filter(self.model.id == identity_id).one()

        except NoResultFound:
            raise IdentityNotFound

        for key, value in params.items():
            if key == 'username':
                continue

            if key == 'password':
                value = self._set_password(value)

            setattr(identity, key, value)

    @singletonmethod
    def change_password(self, identity_id, last_password, password):
        identity = self.get(identity_id)

        if not password_check(identity.password, last_password):
            raise AuthenticationFailed

        identity.password = self._set_password(password)

    @singletonmethod
    def grant_permission(self, permission, identity):
        if permission in identity.permissions:
            raise PermissionAlreadyGranted()
        identity.permissions.append(permission)
