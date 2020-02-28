import logging

import marshmallow
from cornice.resource import resource
from pyramid.httpexceptions import HTTPNoContent
from pyramid.security import Everyone, Allow

from grip.context import SimpleBaseFactory
from grip.decorator import view as grip_view
from grip.resource import BaseResource
from keyloop.api.v1.exceptions import NotFound
from keyloop.schemas.error import ErrorSchema
from keyloop.schemas.identity import IdentitySchema, IdentityUpdateSchema
from keyloop.schemas.path import BasePathSchema

logger = logging.getLogger(__name__)


class IdentityContext(SimpleBaseFactory):
    def __acl__(self):
        # TODO: implement access permission (fixed token?)
        return [(Allow, Everyone, 'edit')]


class CollectionPostAndPutSchema(marshmallow.Schema):
    path = marshmallow.fields.Nested(BasePathSchema)
    body = marshmallow.fields.Nested(IdentitySchema)


class PutSchema(marshmallow.Schema):
    path = marshmallow.fields.Nested(BasePathSchema)
    body = marshmallow.fields.Nested(IdentityUpdateSchema)


class GetAndDeleteSchema(marshmallow.Schema):
    path = marshmallow.fields.Nested(BasePathSchema)


collection_post_response_schemas = {
    200: IdentitySchema(exclude=["password", "permissions"]),
    404: ErrorSchema()
}

get_response_schemas = {
    200: IdentitySchema(exclude=["password"]),
}

collection_delete_put_response_schemas = {
    204: {},
    404: ErrorSchema()
}


@resource(
    collection_path="/realms/{realm_slug}/identities",
    path="/realms/{realm_slug}/identities/{id}",
    content_type="application/vnd.api+json",
    factory=IdentityContext,
)
class IdentityResource(BaseResource):

    @grip_view(schema=CollectionPostAndPutSchema, response_schema=collection_post_response_schemas)
    def collection_post(self):
        validated = self.request.validated["body"]
        identity = self.request.identity_provider.create(
            validated["username"], validated["password"], validated["name"], validated["contacts"]
        )
        return identity

    @grip_view(schema=GetAndDeleteSchema, response_schema=get_response_schemas)
    def get(self):
        """ Return identity info + permissions """
        return self.request.identity_provider.get(self.request.matchdict['id'])

    @grip_view(schema=GetAndDeleteSchema, response_schema=collection_delete_put_response_schemas)
    def delete(self):
        """Remove the identity"""

        self.request.identity_provider.delete(self.request.matchdict['id'])

        return HTTPNoContent()

    @grip_view(schema=PutSchema, response_schema=collection_delete_put_response_schemas)
    def put(self):
        """Update an identity"""
        validated = self.request.validated["body"]

        try:
            self.request.identity_provider.update(self.request.matchdict['id'], params=validated)

            return HTTPNoContent()
        except NotFound:
            self.request.errors.add(
                location='path',
                name='identity_update',
                description='Identity not found'
            )
            self.request.errors.status = 404
