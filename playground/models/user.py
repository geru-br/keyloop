from dataclasses import dataclass

from zope.interface import implementer

from keyloop.interfaces import IIdentity, IIdentitySource


@implementer(IIdentity)
@implementer(IIdentitySource)
@dataclass
class User:
    username: str
    password: str

    def login(self, username, password):
        if password == self.password:
            return self
        return None

    @classmethod
    def  get_echo_user(cls, username):
        return cls(username, password="1234567a")

