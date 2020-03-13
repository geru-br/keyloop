import logging

import marshmallow
from cornice.resource import resource
from pyramid.security import Everyone, Allow

from grip.context import SimpleBaseFactory
from grip.decorator import view as grip_view
from grip.resource import BaseResource, default_error_handler
from keyloop.api.v1.exceptions import IdentityNotFound, PermissionNotFound, PermissionAlreadyGranted
from keyloop.schemas.error import ErrorSchema
from keyloop.schemas.path import BasePathSchema
from keyloop.schemas.permission import PermissionGrantSchema, PermissionSchema

logger = logging.getLogger(__name__)


class PermissionGrantContext(SimpleBaseFactory):
    def __acl__(self):
        return [(Allow, Everyone, 'edit')]


class CollectionPostSchema(marshmallow.Schema):
    path = marshmallow.fields.Nested(BasePathSchema)
    body = marshmallow.fields.Nested(PermissionGrantSchema)


collection_post_response_schemas = {
    200: PermissionSchema,
    404: ErrorSchema(),
    400: ErrorSchema()
}


@resource(
    collection_path="/realms/{realm_slug}/identities/{id}/permissions",
    path="/realms/{realm_slug}/identities/{id}/permissions/{perm_grant_id}",
    content_type="application/vnd.api+json",
    factory=PermissionGrantContext,
)
class PermissionGrantResource(BaseResource):

    @grip_view(schema=CollectionPostSchema,
               response_schema=collection_post_response_schemas,
               error_handler=default_error_handler)
    def collection_post(self):
        validated = self.request.validated
        try:
            identity = self.request.identity_provider.get_by(uuid=validated["path"]["id"])
        except IdentityNotFound:
            self.request.errors.add(
                location='path',
                name='identity_id',
                description='Identity not found'
            )
            self.request.errors.status = 404
            return

        try:
            permission = self.request.permission_provider.get_by(name=validated["body"]["perm_name"])
        except PermissionNotFound:
            self.request.errors.add(
                location='body',
                name='perm_name',
                description='Permission not found'
            )
            return

        try:
            self.request.identity_provider.grant_permission(permission, identity)
        except PermissionAlreadyGranted:
            self.request.errors.add(
                location='body',
                name='perm_name',
                description='Permission already granted to identity'
            )
            return

        return permission
