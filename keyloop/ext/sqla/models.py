import cryptacular.bcrypt
import sqlalchemy as sa
import transaction
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy_utils.types.uuid import UUIDType
from zope.interface import implementer

import uuid

from keyloop.api.v1.exceptions import IdentityNotFound
from keyloop.interfaces.identity import IIdentity, IIdentitySource, IContact
from keyloop.ext.utils.decorators import singleton, singletonmethod


def generate_uuid():
    """Generate an hex representation of an uuid

       :returns: str
    """
    return uuid.uuid4().hex


bcrypt = cryptacular.bcrypt.BCRYPTPasswordManager()


@implementer(IContact)
class Contact:
    __tablename__ = "contact"

    @declared_attr
    def id(self):
        return sa.Column(UUIDType, primary_key=True, default=uuid.uuid4)

    @declared_attr
    def type(self):
        return sa.Column(sa.String, index=True)

    @declared_attr
    def value(self):
        return sa.Column(sa.String, index=True)

    @declared_attr
    def valid_for_auth(self):
        return sa.Column(sa.Boolean, default=False)

    @declared_attr
    def identity_id(self):
        return sa.Column(UUIDType, sa.ForeignKey('identity.id'))

    def identity(self):
        return relationship('RealIdentity', backref=backref('identity', lazy='dynamic'), foreign_keys=[
            self.identity_id])


@implementer(IIdentity)
@singleton
class Identity:
    __tablename__ = "identity"

    @declared_attr
    def id(self):
        return sa.Column(UUIDType, primary_key=True, default=uuid.uuid4)

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
    def get(self, identity_id):
        try:
            return self.session \
                .query(self.model) \
                .filter(self.model.id == identity_id, self.model.active == True) \
                .one()
        except NoResultFound:
            raise IdentityNotFound

    @singletonmethod
    def create(self, username, password, name=None, contacts=None):
        identity = self.model(username=username, password=self._set_password(password), name=name)
        self.session.add(identity)
        self.session.flush()

        for contact in contacts:
            ContactSource.create(contact['type'].value, contact['value'], contact['valid_for_auth'], identity.id)

        transaction.commit()
        return self.session.query(self.model).filter(self.model.username == username).one()

    @singletonmethod
    def delete(self, identity_id):
        identity = self.get(identity_id)

        identity.active = False

        transaction.commit()

    @singletonmethod
    def update(self, identity_id, params):
        try:
            identity = self.session.query(self.model).filter(self.model.id == identity_id).one()

        except NoResultFound:
            raise IdentityNotFound

        for key, value in params.items():
            if key in ('username', 'contacts'):
                continue

            if key == 'password':
                value = self._set_password(value)

            setattr(identity, key, value)

        transaction.commit()


@singleton
class ContactSource:
    def __init__(self, session, model):
        self.model = model
        self.session = session

    @singletonmethod
    def create(self, type, value, valid_for_auth, identity_id):
        contact = self.model(type=type, value=value, valid_for_auth=valid_for_auth, identity_id=identity_id)
        self.session.add(contact)
