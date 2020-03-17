import logging

import marshmallow
from cornice.resource import resource
from pyramid.security import Everyone, Allow

from grip.context import SimpleBaseFactory
from grip.decorator import view as grip_view
from grip.resource import BaseResource, default_error_handler
from keyloop.api.v1.exceptions import PermissionNotFound, PermissionAlreadyGranted
from keyloop.schemas.error import ErrorSchema
from keyloop.schemas.path import IdentityPathSchema
from keyloop.schemas.permission import PermissionGrantSchema, PermissionSchema

logger = logging.getLogger(__name__)


class PermissionGrantContext(SimpleBaseFactory):
    def __acl__(self):
        return [(Allow, Everyone, 'edit')]


class CollectionPostSchema(marshmallow.Schema):
    path = marshmallow.fields.Nested(IdentityPathSchema)
    body = marshmallow.fields.Nested(PermissionGrantSchema)


collection_post_response_schemas = {
    200: PermissionSchema(),
    404: ErrorSchema(),
    400: ErrorSchema()
}


@resource(
    collection_path="/realms/{realm_slug}/identities/{identity_id}/permissions",
    path="/realms/{realm_slug}/identities/{identity_id}/permissions/{perm_grant_id}",
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
            permission = self.request.permission_provider.get(name=validated["body"]["perm_name"])
        except PermissionNotFound:
            self.request.errors.add(
                location='body',
                name='perm_name',
                description='Permission not found'
            )
            return

        try:
            self.request.identity_provider.grant_permission(permission, self.request.identity)
        except PermissionAlreadyGranted:
            # XXX Guilherme: in this scenario we return the same response as
            # the first time a permission is granted. This solution provides
            # better caching management on the client's side when it is
            # attempting to grant the same permission twice for some identity.
            logger.info("Identity already have this permission")

        return permission
