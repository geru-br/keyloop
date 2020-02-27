import json

import marshmallow
from cornice.resource import resource
from pyramid.httpexceptions import HTTPAccepted, HTTPOk, HTTPNotFound, HTTPBadRequest
from pyramid.security import remember, forget, Everyone, Allow

from grip.context import SimpleBaseFactory
from grip.decorators import grip_view
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
    200: AuthSessionSchema(exclude=["identity.password"], include_data=["identity"]),
    404: AuthSessionSchema(exclude=["identity.password"], include_data=["identity"])
}


def validate_get(request, **kwargs):
    #raise HTTPNotFound()
    #request.errors.add("body", "realm_slug", "Realm does not exist")
    pass


def get_error_handler(request):

    response = request.response

    import json
    response.body = json.dumps(request.errors[0]).encode("utf-8")
    response.status_code = request.errors.status
    response.content_type = 'application/vnd.api+json'
    return response


@resource(
    collection_path="/realms/{realm_slug}/auth-session",
    path="/realms/{realm_slug}/auth-session/{id}",
    content_type="application/vnd.api+json",
    factory=AuthSessionContext,
)
class AuthSessionResource(BaseResource):
    # collection_post_schema = CollectionPostSchema
    # collection_response_schemas = collection_response_schemas
    resource_get_schema = marshmallow.Schema

    @grip_view(schema=CollectionPostSchema, response_schema=collection_response_schemas)
    def collection_post(self):
        # where is this property being set?
        # should we define a property direct on the factory context
        import pytest; pytest.set_trace()
        validated = self.request.validated["body"]

        username = validated["username"]

        headers = remember(self.request, username)
        self.request.response.headers.extend(headers)

        return self.request.auth_session

    @grip_view(validators=validate_get, error_handler=get_error_handler)
    def get(self):
        """ Return identity info + permissions """

        # auth_session_id = self.request.validated["path"]["id"]

        # session = AuthSession.get_session(id, realm)

        # identity = Identity.get_identity(realm, username)

        # session = AuthSession(username, password, identity)

        # return session

        # TODO: fetch permisionn
        return HTTPOk()

    def delete(self):
        """ Logout """

        # Should we trigger notifications to other services?
        forget(self.request)

        return HTTPAccepted()
