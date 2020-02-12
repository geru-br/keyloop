"""
Zope Adapter snippet

"""


from zope.interface import implementer, implementedBy, Interface, Attribute
from zope.interface.adapter import AdapterRegistry

from dataclasses import dataclass

import typing as T

# ----- Kloop - tem que ser um "singleton" - provavelmente dentro do pyramidconfig
registry = AdapterRegistry()

#--------- Kloop
class IIdentity(Interface):
    prenome = Attribute("")
    sobrenome = Attribute("")
#===================================


#-------- EXTERNAL_APP
class IUser(Interface):
    nome = Attribute("")
#===================================

#--------- EXTERNAL_APP
@implementer(IUser)
@dataclass
class User:    
    nome: str
    @property
    def prenome(self): pass

    @property
    def sobrenome(self): pass
#--------- EXTERNAL_APP
class AdapterUserIdentity:registry = AdapterRegistry() registry = AdapterRegistry() 
    def __init__(self, user):
        self.prenome = user.nome.split()[0]
        self.sobrenome = user.nome.split()[-1]

# EXTERNAL_APP - 
registry.register([IUser], IIdentity, '', AdapterUserIdentity)


u = User("Joao Bueno")

# KLoop
def funcao_muito_louca_que_precisa_de_um_identity(obj: T.Any):

    cls = type(obj)
    adapter = registry.lookup(implementedBy(cls), IIdentity, '') 
    final_identity_obj = adapter(obj)

    final_identity_obj.prenome



# Kloop - usado no EXTERNAL_APP para dizer qual é a fonte de dados de Identity
class IIdentitySource(Interface):
    """Marker interface for callables that retrieve an Identity object given a username
    """
    def __call__(username) -> Identity:
        pass

# EXTERNAL_APP
def get_user_from_db(username):
    db_session = # conecta no DB da app-externa com os usuarios
    user  = User.get(username)
    return AdapterUserIdentity(user)

# EXTERNAL_APP
from kloop import IdentitySource
registry.register([IIdentitySource], IIdentity, 'CORE-REALM', get_user_from_db) 

# dentro das classes que vão responder aos clientes
registry.register([IIdentitySource], IIdentity, 'CLIENT-REALM', funcao_que_busca_user_em_outro_db) 
...
# Kloop
    def collection_post(self):

        realm = self.request.validated["path"]["realm_slug"]
        validated = self.request.validated["body"]

        username = validated["username"]
        password = validated["password"]
        
        
        identity = registry.lookup(IIdentitySource, IIdentity, realm)(username)

        session = AuthSession(username, password, identity)

        remember(self.request, username, policy_name='kloop')

        return session
