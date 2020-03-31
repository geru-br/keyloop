import logging

import marshmallow
from cornice.resource import resource
from pyramid.httpexceptions import HTTPNoContent
from pyramid.security import remember, forget, Everyone, Allow

from grip.context import SimpleBaseFactory
from grip.decorator import view as grip_view
from grip.resource import BaseResource, default_error_handler
from keyloop.api.v1.exceptions import IdentityNotFound, AuthenticationFailed
from keyloop.schemas.auth_session import AuthSessionSchema
from keyloop.schemas.path import BasePathSchema

logger = logging.getLogger(__name__)


class AuthSessionContext(SimpleBaseFactory):
    def __acl__(self):
        # TODO: implement access permission (fixed token?)
        return [(Allow, Everyone, "edit")]


collection_response_schemas = {
    200: AuthSessionSchema(exclude=["identity.password"], include_data=["identity"]),
    204: None,
    401: AuthSessionSchema(exclude=["identity.password"], include_data=["identity"]),
    404: AuthSessionSchema(exclude=["identity.password"], include_data=["identity"]),
}


class BaseValidatedSchema(marshmallow.Schema):
    path = marshmallow.fields.Nested(BasePathSchema)


class CollectionPostSchema(marshmallow.Schema):
    path = marshmallow.fields.Nested(BasePathSchema)
    body = marshmallow.fields.Nested(AuthSessionSchema(exclude=["identity"]))


@resource(
    collection_path="/realms/{realm_slug}/auth-session",
    path="/realms/{realm_slug}/auth-session/{id}",
    content_type="application/vnd.api+json",
    factory=AuthSessionContext,
)
class AuthSessionResource(BaseResource):
    @grip_view(
        schema=CollectionPostSchema,
        response_schema=collection_response_schemas,
        error_handler=default_error_handler,
    )
    def collection_post(self):
        params = self.request.validated['body']
        try:
            new_session = self.request.auth_session.login(params['username'], params['password'])
        except IdentityNotFound:
            msg = 'User not found'
            self.request.errors.add(
                location='body',
                name='username',
                description=msg
            )
            self.request.errors.status = 404
            logger.info(msg)

        except AuthenticationFailed:
            msg = 'Username or password are incorrect'
            self.request.errors.add(
                location='body',
                name='login',
                description=msg
            )
            self.request.errors.status = 401
            logger.info(msg)

        else:
            headers = remember(self.request, params['username'])
            self.request.response.headers.extend(headers)
            return new_session

    @grip_view(
        schema=BaseValidatedSchema,
        response_schema=collection_response_schemas,
        error_handler=default_error_handler,
    )
    def collection_get(self):
        """ Return identity info + permissions """
        try:
            return self.request.auth_session.get_identity(self.request.authenticated_userid)

        except IdentityNotFound:
            msg = 'Auth session not found'
            self.request.errors.add(
                location='header',
                name='retrieve_auth_session',
                description=msg
            )
            self.request.errors.status = 404
            logger.info(msg)

    @grip_view(
        schema=BaseValidatedSchema,
        response_schema=collection_response_schemas,
        error_handler=default_error_handler,
    )
    def delete(self):
        """ Logout"""
        headers = forget(self.request)
        self.request.response.headers.extend(headers)
        return HTTPNoContent()
