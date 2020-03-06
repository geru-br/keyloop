import logging

import marshmallow
from cornice.resource import resource
from pyramid.security import Everyone, Allow

from grip.context import SimpleBaseFactory
from grip.decorator import view as grip_view
from grip.resource import BaseResource, default_error_handler
from keyloop.schemas.path import BasePathSchema
from keyloop.schemas.permission import PermissionSchema

logger = logging.getLogger(__name__)


class PermissionContext(SimpleBaseFactory):
    def __acl__(self):
        return [(Allow, Everyone, 'edit')]


class CollectionPostPermissionSchema(marshmallow.Schema):
    path = marshmallow.fields.Nested(BasePathSchema)
    body = marshmallow.fields.Nested(PermissionSchema)


collection_post_response_schemas = {
    200: PermissionSchema(),
}


@resource(
    collection_path="/realms/{realm_slug}/permissions",
    path="/realms/{realm_slug}/permissions/{id}",
    content_type="application/vnd.api+json",
    factory=PermissionContext,
)
class PermissionResource(BaseResource):

    @grip_view(schema=CollectionPostPermissionSchema, response_schema=collection_post_response_schemas,
               error_handler=default_error_handler)
    def collection_post(self):
        validated = self.request.validated["body"]
        permission = self.request.permission_provider.create(validated["name"], validated["description"])
        return permission
