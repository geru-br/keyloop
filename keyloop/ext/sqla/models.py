import sqlalchemy as sa
import transaction
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship, backref
from zope.interface import implementer

from keyloop.interfaces.identity import IIdentity, IIdentitySource, IContact
from keyloop.ext.utils.decorators import singleton, singletonmethod


@implementer(IContact)
class Contact:
    __tablename__ = "contact"

    @declared_attr
    def id(self):
        return sa.Column(sa.Integer, autoincrement=True, primary_key=True)

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
        return sa.Column(sa.Integer, sa.ForeignKey('identity.id'))

    # TODO: Make this attribute available on response schema
    def contacts(self):
        return relationship('Identity', backref=backref('contacts', lazy='dynamic'), foreign_keys=[self.identity_id])


@implementer(IIdentity)
@singleton
class Identity():
    __tablename__ = "identity"

    @declared_attr
    def id(self):
        return sa.Column(sa.Integer, autoincrement=True, primary_key=True)

    @declared_attr
    def username(self):
        return sa.Column(sa.String, index=True)

    @declared_attr
    def password(self):
        return sa.Column(sa.String, index=True)

    @declared_attr
    def name(self):
        return sa.Column(sa.String)

    @singletonmethod
    def login(self, username, password):
        return IdentitySource.get(username)


@implementer(IIdentitySource)
@singleton
class IdentitySource:
    def __init__(self, session, model):
        self.model = model
        self.session = session

    @singletonmethod
    def get(self, username):
        return self.session.query(self.model).filter(self.model.username == username).one()

    @singletonmethod
    def create(self, username, password, name=None, contacts=None):
        identity = self.model(username=username, password=password, name=name)
        self.session.add(identity)
        self.session.flush()

        for contact in contacts:
            ContactSource.create(contact['type'].value, contact['value'], contact['valid_for_auth'], identity.id)

        transaction.commit()
        return self.get(username)


@singleton
class ContactSource:
    def __init__(self, session, model):
        self.model = model
        self.session = session

    @singletonmethod
    def create(self, type, value, valid_for_auth, identity_id):
        contact = self.model(type=type, value=value, valid_for_auth=valid_for_auth, identity_id=identity_id)
        self.session.add(contact)
