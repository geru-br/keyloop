import json

import marshmallow
from cornice.resource import resource
from pyramid.security import remember, forget, Everyone, Allow

import arrow
from grip.context import SimpleBaseFactory
from grip.decorator import view as grip_view
from grip.resource import BaseResource, default_error_handler
from keyloop.interfaces.auth_session import IAuthSession, IAuthSessionSource
from keyloop.interfaces.identity import IIdentity, IIdentitySource
from keyloop.schemas.auth_session import AuthSessionSchema


class AuthSessionContext(SimpleBaseFactory):
    def __acl__(self):
        # TODO: implement access permission (fixed token?)
        return [(Allow, Everyone, "edit")]


collection_response_schemas = {
    200: AuthSessionSchema(exclude=["identity.password"], include_data=["identity"]),
    204: AuthSessionSchema(exclude=["identity.password"], include_data=["identity"]),
    401: AuthSessionSchema(exclude=["identity.password"], include_data=["identity"]),
    404: AuthSessionSchema(exclude=["identity.password"], include_data=["identity"]),
}


def validate_realm_and_id(request, **kwargs):
    id = request.matchdict["id"]
    realm_slug = request.matchdict["realm_slug"]

    registry = request.registry.settings["keyloop_adapters"]

    identity_provider = registry.lookup([IIdentity], IIdentitySource, realm_slug)
    if not identity_provider:
        request.errors.add("body", "realm_slug", "Realm does not exist")
        request.errors.status = 404
        return

    session_provider = registry.lookup([IAuthSession], IAuthSessionSource, realm_slug)
    auth_session = session_provider.get(id)

    request.auth_session = auth_session


def validate_login(request, **kwargs):
    registry = request.registry.settings["keyloop_adapters"]

    login_schema = AuthSessionSchema(exclude=["ttl", "active"])
    login_schema.context = request.context
    data = login_schema.load(request.json)[0]

    identity_provider = registry.lookup(
        [IIdentity], IIdentitySource, request.context.realm
    )

    if not identity_provider:
        request.errors.add("body", "realm_slug", "Realm does not exist")
        request.errors.status = 404
        return

    identity = identity_provider.get(data["username"])

    if not identity.login(data["username"], data["password"]):
        request.errors.add("body", "login", "User name or password are incorrect")
        request.errors.status = 401
        return

    session_provider = registry.lookup(
        [IAuthSession], IAuthSessionSource, request.context.realm
    )

    auth_session = session_provider.create(
        identity=identity, ttl=600, active=True, start=arrow.utcnow().datetime
    )

    request.identity = identity
    request.auth_session = auth_session


@resource(
    collection_path="/realms/{realm_slug}/auth-session",
    path="/realms/{realm_slug}/auth-session/{id}",
    content_type="application/vnd.api+json",
    factory=AuthSessionContext,
)
class AuthSessionResource(BaseResource):
    @grip_view(
        validators=validate_login,
        response_schema=collection_response_schemas,
        error_handler=default_error_handler,
    )
    def collection_post(self):
        auth_session = self.request.auth_session
        username = auth_session.identity.username

        headers = remember(self.request, username)
        self.request.response.headers.extend(headers)

        return self.request.auth_session

    @grip_view(
        validators=validate_realm_and_id,
        response_schema=collection_response_schemas,
        error_handler=default_error_handler,
    )
    def get(self):
        """ Return identity info + permissions """
        return self.request.auth_session

    @grip_view(
        validators=validate_realm_and_id,
        response_schema=collection_response_schemas,
        error_handler=default_error_handler,
    )
    def delete(self):
        """ Logout """
        # Should we trigger notifications to other services?
        auth_session = self.request.auth_session
        forget(self.request)
        auth_session.delete()
