import marshmallow
from cornice.resource import resource
from pyramid.httpexceptions import HTTPAccepted
from pyramid.security import remember, forget, Everyone, Allow
from zope.interface.adapter import AdapterRegistry

from grip.context import SimpleBaseFactory
from grip.resource import BaseResource
from keyloop.interfaces import IdentityDummyAdapter, IIdentitySource, IIdentity
from keyloop.models.auth_session import AuthSession
from keyloop.schemas.auth_session import AuthSessionSchema
from keyloop.schemas.path import BasePathSchema

registry = AdapterRegistry()


class AuthSessionContext(SimpleBaseFactory):
    def __acl__(self):
        # TODO: implement access permission (fixed token?)
        return [(Allow, Everyone, 'edit')]


class CollectionPostSchema(marshmallow.Schema):
    path = marshmallow.fields.Nested(BasePathSchema)
    body = marshmallow.fields.Nested(AuthSessionSchema(exclude=["identity"]))


collection_response_schemas = {200: AuthSessionSchema(exclude=["username", "password"])}


@resource(
    collection_path="/realms/{realm_slug}/auth-session",
    path="/realms/{realm_slug}/auth-session/{id}",
    content_type="application/vnd.api+json",
    factory=AuthSessionContext,
)
class AuthSessionResource(BaseResource):
    collection_post_schema = CollectionPostSchema
    collection_response_schemas = collection_response_schemas

    def collection_post(self):
        # where is this property being set?
        # should we define a property direct on the factory context

        realm = self.request.validated["path"]["realm_slug"]
        validated = self.request.validated["body"]

        username = validated["username"]
        password = validated["password"]

        registry.register([IIdentitySource], IIdentity, realm, IdentityDummyAdapter)
        identity = registry.lookup([IIdentitySource], IIdentity, realm)(username)
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

        return {}

    def delete(self):
        """ Logout """

        # Should we trigger notifications to other services?
        forget(self.request)

        return HTTPAccepted()