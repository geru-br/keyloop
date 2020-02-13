import marshmallow
from cornice.resource import resource
from pyramid.httpexceptions import HTTPAccepted
from pyramid.security import remember, forget
from zope.interface.adapter import AdapterRegistry

from grip.context import SimpleBaseFactory
from grip.resource import BaseResource
from keyloop.interfaces import IIdentitySource, IIdentity
from keyloop.models.auth_session import AuthSession
from keyloop.schemas.auth_session import AuthSessionSchema
from keyloop.schemas.path import BasePathSchema

registry = AdapterRegistry()


class AuthSessionContext(SimpleBaseFactory):

    def __acl__(self):
        # TODO: implement access permission (fixed token?)
        pass


class CollectionPostSchema(marshmallow.Schema):
    path = marshmallow.fields.Nested(BasePathSchema)
    body = marshmallow.fields.Nested(AuthSessionSchema(exclude=["identity"]))


collection_response_schemas = {200: AuthSessionSchema(exclude=["username", "password"])}


@resource(
    collection_path="/api/v1/realms/{realm_slug}/auth-session",
    path="/api/v1/realms/{realm_slug}/auth-session/{id}",
    content_type="application/json",
    factory=AuthSessionContext,
)
class AuthSession(BaseResource):
    collection_post_schema = CollectionPostSchema
    collection_response_schemas = collection_response_schemas

    def collection_post(self):
        realm = self.request.validated["path"]["realm_slug"]
        validated = self.request.validated["body"]

        username = validated["username"]
        password = validated["password"]

        identity = registry.lookup(IIdentitySource, IIdentity, realm)(username)
        identity.login(password)

        session = AuthSession(username, password, identity)

        remember(self.request, username, policy_name='kloop')

        return session

    def get(self):
        """ Return identity info + permissions """

        # realm = self.request.validated["path"]["realm_slug"]
        # id = self.request.validated["path"]["id"]

        # # session = AuthSession.get_session(id, realm)

        # identity = Identity.get_identity(realm, username)

        # session = AuthSession(username, password, identity)

        # return session

        # TODO: fetch permisions

        pass

    def delete(self):
        """ Logout """

        # Should we trigger notifications to other services?
        forget(self.request)

        return HTTPAccepted()
