import json

import marshmallow
from cornice.resource import resource
from pyramid.httpexceptions import HTTPAccepted, HTTPOk, HTTPNotFound, HTTPBadRequest
from pyramid.security import remember, forget, Everyone, Allow

from grip.context import SimpleBaseFactory
from grip.decorator import view as grip_view
from grip.resource import BaseResource
from keyloop.interfaces.auth_session import IAuthSession, IAuthSessionSource
from keyloop.interfaces.identity import IIdentity, IIdentitySource
from keyloop.schemas.auth_session import AuthSessionSchema
from keyloop.schemas.path import BasePathSchema


class AuthSessionContext(SimpleBaseFactory):
    def __acl__(self):
        # TODO: implement access permission (fixed token?)
        return [(Allow, Everyone, "edit")]


class CollectionPostSchema(marshmallow.Schema):
    path = marshmallow.fields.Nested(BasePathSchema)
    body = marshmallow.fields.Nested(AuthSessionSchema(exclude=["identity"]))


class ResourceGetSchema(marshmallow.Schema):
    path = marshmallow.fields.Nested(BasePathSchema)


collection_response_schemas = {
    200: AuthSessionSchema(exclude=["identity.password"], include_data=["identity"]),
    404: AuthSessionSchema(exclude=["identity.password"], include_data=["identity"])
}


def validate_get(request, **kwargs):
    #raise HTTPNotFound()
    #request.errors.add("body", "realm_slug", "Realm does not exist")

    import pytest; pytest.set_trace()
    id = request.matchdict['id']
    realm_slug = request.matchdict['realm_slug']

    registry = request.registry.settings["keyloop_adapters"]

    identity_provider = registry.lookup(
        [IIdentity], IIdentitySource, realm_slug
    )
    if not identity_provider:
        request.errors.status = 404
        return

    session_provider = registry.lookup(
        [IAuthSession], IAuthSessionSource, realm_slug
    )
    auth_session = session_provider.get(id)

    request.auth_session = auth_session

    # identity = identity_provider.get(data["username"])
    #
    # if not identity.login(data["username"], data["password"]):
    #     # need to find a way to return a 401 instead of a 400
    #     raise marshmallow.ValidationError("credentials failed")
    #
    # session_provider = registry.lookup(
    #     [IAuthSession], IAuthSessionSource, request.context.realm
    # )


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

    @grip_view(schema=CollectionPostSchema, response_schema=collection_response_schemas)
    def collection_post(self):
        # where is this property being set?
        # should we define a property direct on the factory context

        validated = self.request.validated["body"]

        username = validated["username"]

        headers = remember(self.request, username)
        self.request.response.headers.extend(headers)

        return self.request.auth_session

    @grip_view(validators=validate_get, error_handler=get_error_handler, response_schema=collection_response_schemas)
    def get(self):
        """ Return identity info + permissions """
        return self.request.auth_session

    def delete(self):
        """ Logout """

        # Should we trigger notifications to other services?
        forget(self.request)

        return HTTPAccepted()
