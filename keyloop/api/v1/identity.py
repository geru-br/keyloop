import logging

import marshmallow
from cornice.resource import resource
from pyramid.httpexceptions import HTTPNoContent
from pyramid.security import Everyone, Allow, forget

from grip.context import SimpleBaseFactory
from grip.decorator import view as grip_view
from grip.resource import BaseResource, default_error_handler
from keyloop.api.v1.exceptions import AuthenticationFailed, IdentityAlreadyExists
from keyloop.schemas.error import ErrorSchema
from keyloop.schemas.identity import IdentitySchema, IdentityUpdateSchema, IdentityUpdatePasswordSchema
from keyloop.schemas.path import BasePathSchema, IdentityPathSchema

logger = logging.getLogger(__name__)


class IdentityContext(SimpleBaseFactory):
    def __acl__(self):
        # TODO: implement access permission (fixed token?)
        return [(Allow, Everyone, 'edit')]


class CollectionPostSchema(marshmallow.Schema):
    path = marshmallow.fields.Nested(BasePathSchema)
    body = marshmallow.fields.Nested(IdentitySchema)


class PatchSchema(marshmallow.Schema):
    path = marshmallow.fields.Nested(IdentityPathSchema)
    body = marshmallow.fields.Nested(IdentityUpdateSchema)


class PatchPasswordSchema(marshmallow.Schema):
    path = marshmallow.fields.Nested(IdentityPathSchema)
    body = marshmallow.fields.Nested(IdentityUpdatePasswordSchema(
        exclude=['name', 'active', 'permissions']
    ))


class GetAndDeleteSchema(marshmallow.Schema):
    path = marshmallow.fields.Nested(IdentityPathSchema)


collection_post_response_schemas = {
    200: IdentitySchema(exclude=["password", "permissions"]),
    404: ErrorSchema()
}

get_response_schemas = {
    200: IdentitySchema(exclude=["password"]),
}

collection_delete_patch_response_schemas = {
    204: None,
    404: ErrorSchema()
}


@resource(
    collection_path="/realms/{realm_slug}/identities",
    path="/realms/{realm_slug}/identities/{identity_id}",
    content_type="application/vnd.api+json",
    factory=IdentityContext,
)
class IdentityResource(BaseResource):

    @grip_view(schema=CollectionPostSchema, response_schema=collection_post_response_schemas,
               error_handler=default_error_handler)
    def collection_post(self):
        validated = self.request.validated["body"]
        try:
            identity = self.request.identity_provider.create(
                validated["username"], validated["password"], validated["name"],
            )
        except IdentityAlreadyExists:
            msg = 'Username already exists'
            self.request.errors.add(
                location='path',
                name='identity_create',
                description=msg
            )
            self.request.errors.status = 409
            logger.info(msg)

        else:
            return identity

    @grip_view(schema=GetAndDeleteSchema, response_schema=get_response_schemas)
    def get(self):
        """ Return identity info + permissions """
        return self.request.identity

    @grip_view(schema=GetAndDeleteSchema, response_schema=collection_delete_patch_response_schemas)
    def delete(self):
        """Remove the identity"""

        self.request.identity_provider.delete(self.request.identity)
        headers = forget(self.request)
        self.request.response.headers.extend(headers)
        return HTTPNoContent()

    @grip_view(schema=PatchSchema, response_schema=collection_delete_patch_response_schemas)
    def patch(self):
        """Update an identity"""
        validated = self.request.validated["body"]
        self.request.identity_provider.update(self.request.identity, params=validated)
        return HTTPNoContent()


@resource(
    path="/realms/{realm_slug}/identities/{identity_id}/password",
    content_type="application/vnd.api+json",
    factory=IdentityContext,
)
class IdentityPasswordResource(BaseResource):
    @grip_view(schema=PatchPasswordSchema, response_schema=collection_delete_patch_response_schemas)
    def patch(self):
        """Update the password identity"""
        validated = self.request.validated["body"]

        try:
            self.request.identity_provider.change_password(self.request.identity,
                                                           validated['last_password'],
                                                           validated['password'])
            return HTTPNoContent()
        except AuthenticationFailed:
            msg = 'Last password did not match'
            self.request.errors.add(
                location='body',
                name='last_password',
                description=msg
            )
            self.request.errors.status = 401
            logger.info('Last password did not match')
