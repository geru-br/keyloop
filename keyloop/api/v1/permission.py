import logging

import marshmallow
from cornice.resource import resource
from pyramid.security import Everyone, Allow

from grip.context import SimpleBaseFactory
from grip.decorator import view as grip_view
from grip.resource import BaseResource, default_error_handler
from keyloop.api.v1.exceptions import PermissionAlreadyExists
from keyloop.schemas.error import ErrorSchema
from keyloop.schemas.path import BasePathSchema
from keyloop.schemas.permission import PermissionSchema, PermissionQueryStringSchema, PermissionsListSchema

logger = logging.getLogger(__name__)

MAX_ROWS_PER_PAGE = 30


class PermissionContext(SimpleBaseFactory):
    def __acl__(self):
        return [(Allow, Everyone, "edit")]


class CollectionPostSchema(marshmallow.Schema):
    path = marshmallow.fields.Nested(BasePathSchema)
    body = marshmallow.fields.Nested(PermissionSchema(exclude=['document_meta']))


class CollectionGetSchema(marshmallow.Schema):
    path = marshmallow.fields.Nested(BasePathSchema)
    querystring = marshmallow.fields.Nested(PermissionQueryStringSchema)


collection_post_response_schemas = {
    200: PermissionSchema(),
    400: ErrorSchema()
}

collection_get_response_schemas = {
    200: PermissionsListSchema(),
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
            msg = f"Existent permission with name: {params['name']}"
            self.request.errors.add(
                location="body",
                name="name",
                description=msg
            )
            logger.info(msg)

    @grip_view(schema=CollectionGetSchema, response_schema=collection_get_response_schemas)
    def collection_get(self):
        params = self.request.validated["querystring"]
        page = params['page'] if 'page' in params else 1
        limit = params['limit'] if 'limit' in params else MAX_ROWS_PER_PAGE

        # TODO: Adjust the grip for mount the pages link. The marshmallow json-api doesn't do it yet
        return self.request.permission_provider.list(page, limit)
