import cryptacular.bcrypt
from sqlalchemy.orm.exc import NoResultFound
from zope.interface import implementer

from keyloop.api.v1.exceptions import IdentityNotFound, AuthenticationFailed
from keyloop.ext.utils.decorators import singleton, singletonmethod
from keyloop.interfaces.auth_session import IAuthSessionSource

bcrypt = cryptacular.bcrypt.BCRYPTPasswordManager()


def password_check(password_field, value):
    return bcrypt.check(password_field, value)


@implementer(IAuthSessionSource)
@singleton
class AuthSessionSource:
    model = None
    session = None

    def __init__(self, session, model):
        self.model = model
        self.session = session

    @singletonmethod
    def _get_identity_by(self, username):
        try:
            return self.session.query(self.model).filter(self.model.username == username,
                                                         self.model.active == True).one()

        except NoResultFound:
            raise IdentityNotFound

    @singletonmethod
    def get_identity(self, username):
        return {'identity': self._get_identity_by(username)}

    @singletonmethod
    def login(self, username, password):
        identity = self._get_identity_by(username)

        if not password_check(identity.password, password):
            raise AuthenticationFailed

        return {'identity': identity}
