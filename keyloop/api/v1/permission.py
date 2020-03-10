import logging

import marshmallow
from cornice.resource import resource
from pyramid.security import Everyone, Allow

from grip.context import SimpleBaseFactory
from grip.decorator import view as grip_view
from grip.resource import BaseResource, default_error_handler
from keyloop.api.v1.exceptions import PermissionAlreadyExists
from keyloop.schemas.path import BasePathSchema
from keyloop.schemas.permission import PermissionSchema

logger = logging.getLogger(__name__)


class PermissionContext(SimpleBaseFactory):
    def __acl__(self):
        return [(Allow, Everyone, "edit")]


class CollectionPostSchema(marshmallow.Schema):
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

    @grip_view(schema=CollectionPostSchema, response_schema=collection_post_response_schemas,
               error_handler=default_error_handler)
    def collection_post(self):
        params = self.request.validated["body"]

        try:
            permission = self.request.permission_provider.create(params["name"], params["description"])
            return permission
        except PermissionAlreadyExists:
            self.request.errors.add(
                location="body",
                name="name",
                description=f"Existent permission with name: {params['name']}"
            )
