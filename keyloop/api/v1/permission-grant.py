import logging

import marshmallow
from cornice.resource import resource
from pyramid.security import Everyone, Allow

from grip.context import SimpleBaseFactory
from grip.decorator import view as grip_view
from grip.resource import BaseResource, default_error_handler
from keyloop.schemas.path import BasePathSchema
from keyloop.schemas.permission import PermissionGrantSchema

logger = logging.getLogger(__name__)


class PermissionGrantContext(SimpleBaseFactory):
    def __acl__(self):
        return [(Allow, Everyone, 'edit')]


class CollectionPostSchema(marshmallow.Schema):
    path = marshmallow.fields.Nested(BasePathSchema)
    body = marshmallow.fields.Nested(PermissionGrantSchema)


collection_post_response_schemas = {
    200: PermissionGrantSchema
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
        identity = self.request.identity_provider.get(validated["path"]["id"])
        permission = self.request.permission_provider.get(name=validated["body"]["perm_name"])
        perm_grant = self.request.perm_grant_provider.create(permission.uuid, identity.id)
        return perm_grant
