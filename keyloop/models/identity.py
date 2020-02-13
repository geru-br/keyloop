# from zope.interface import implements
# from keyloop.interfaces import IIdentity
#
# @implements(IIdentity)
# class Identity:
#
#     @classmethod
#     def get_identity(cls, realm_slug, username):
#         # how to filter an identity and check if it is from the receved realm?
#         return cls.query.filter(realm_slug=realm_slug, username=username).first()

"""
abstract IdentityBla

    keyloop
        models
            realm
            identity

        realm 1 -- * identity

    loan-request
        user (username, password)




Sugetão: usar adapters do zope.interface  .

Com isso, podemos criar uma adapter da interface do objeto User do loans-request (
    tem que escrever essa interface "IUser" - para a interface "IIdentity" - 

)
No código do EXTERNAL_APP, registramos esse adapter - No código do kloop, ele pega
"um objeto qualquer" e chama a funcionalidade de uso dos adapters do zope.interface -
- isso localiza automaticamente o adapter registrado no EXTERNAL_APP, e devove um objeto
que tem a interface IIdentity



"""