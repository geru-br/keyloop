import marshmallow
from cornice.resource import resource
from pyramid.httpexceptions import HTTPAccepted
from pyramid.security import remember, forget, Everyone, Allow

from grip.context import SimpleBaseFactory
from grip.resource import BaseResource
from keyloop.schemas.auth_session import AuthSessionSchema
from keyloop.schemas.path import BasePathSchema


class AuthSessionContext(SimpleBaseFactory):
    def __acl__(self):
        # TODO: implement access permission (fixed token?)
        return [(Allow, Everyone, "edit")]


class CollectionPostSchema(marshmallow.Schema):
    path = marshmallow.fields.Nested(BasePathSchema)
    body = marshmallow.fields.Nested(AuthSessionSchema(exclude=["identity"]))


collection_response_schemas = {
    200: AuthSessionSchema(exclude=["identity.password"], include_data=["identity"])
}


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

        validated = self.request.validated["body"]

        import pdb
        pdb.set_trace()
        username = validated["username"]

        headers = remember(self.request, username)
        self.request.response.headers.extend(headers)

        return self.request.auth_session

    def get(self):
        """ Return identity info + permissions """

        # auth_session_id = self.request.validated["path"]["id"]

        # session = AuthSession.get_session(id, realm)

        # identity = Identity.get_identity(realm, username)

        # session = AuthSession(username, password, identity)

        # return session

        # TODO: fetch permisionn
        return {}

    def delete(self):
        """ Logout """

        # Should we trigger notifications to other services?
        forget(self.request)

        return HTTPAccepted()
