from zope.interface import (
    Interface,
    Attribute
)

# /realms/{realm_slug}/identities/{identificador}
#     PUT/PATCH: atualiza identificador (funcionalidade "troca senha" fica aqui???)
#     POST: recebe action e atualiza estado (semântica adotada pela Geru referente ao POST)
#     DELETE: deleta identidade (soft delete)
#     GET: retorna info da identidade + permissões

class IIdentity(Interface):
    password = Attribute('The password for verifying the user')

    def login(password) -> bool:
        """Verify the identity
        """
        pass


class IIdentitySource(Interface):
    """Marker interface for callables that retrieve an Identity object given a username
    """
    def __call__(username) -> IIdentity:
        pass 