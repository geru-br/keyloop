from dataclasses import dataclass

from zope.interface import implementer

from keyloop.interfaces.identity import IIdentity, IIdentitySource


@implementer(IIdentity)
@implementer(IIdentitySource)
@dataclass
class User:
    username: str
    password: str
    name: str = None

    def login(self, username, password):
        if password == self.password:
            return self
        return None

    @classmethod
    def  get(cls, username):
        return cls(username, password="1234567a", name=f"{username} {username}")

    @classmethod
    def create(cls, username, password, name, contacts):
        import json
        with open(username, 'w') as fp:
            json.dump({
                'password':password,
                'name': name,
                'contact': contacts
            }, fp)
