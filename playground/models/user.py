from dataclasses import dataclass

from zope.interface import implementer

from keyloop.interfaces import IIdentity, IIdentitySource


@implementer(IIdentity)
@dataclass
class User:
    username: str
    password: str

    def login(self, username, password):
        if password == self.password:
            return self
        return None



@implementer(IIdentitySource)
def  echo_user_provider(username):
    return User(username, password="1234567a")