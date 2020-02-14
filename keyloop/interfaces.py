from zope.interface import (
    implementer,
    Interface,
    Attribute
)

# /realms/{realm_slug}/identities/{identificador}
#     PUT/PATCH: atualiza identificador (funcionalidade "troca senha" fica aqui???)
#     POST: recebe action e atualiza estado (semântica adotada pela Geru referente ao POST)
#     DELETE: deleta identidade (soft delete)
#     GET: retorna info da identidade + permissões


class IIdentity(Interface):
    username = Attribute('Unique string used for identifying a user party.')
    password = Attribute('The password for verifying the user')

    def login(username, password) -> bool:
        """Verify the identity."""
        pass


class IIdentitySource(Interface):
    """Marker interface for callables that retrieve an Identity object given a username
    """
    def __call__(username) -> IIdentity:
        pass


@implementer(IIdentitySource)
class IdentityDummyAdapter:

    def __init__(self, username):
        self.username = username
        self._query_password()

    def login(self, password) -> bool:
        """Verify the identity
        """
        if self.password == password:
            print("freaking passowrd is right")
            return True

        print("freaking passowrd is wrong")
        return False

    def _query_password(self):
        self.password = "blablabla"
