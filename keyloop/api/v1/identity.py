import logging

import marshmallow
from cornice.resource import resource
from pyramid.httpexceptions import HTTPNoContent
from pyramid.security import forget, Everyone, Allow

from grip.context import SimpleBaseFactory
from grip.decorator import view as grip_view
from grip.resource import BaseResource
from keyloop.schemas.error import ErrorSchema
from keyloop.schemas.identity import IdentitySchema
from keyloop.schemas.path import BasePathSchema

logger = logging.getLogger(__name__)


class IdentityContext(SimpleBaseFactory):
    def __acl__(self):
        # TODO: implement access permission (fixed token?)
        return [(Allow, Everyone, 'edit')]


class CollectionPostSchema(marshmallow.Schema):
    path = marshmallow.fields.Nested(BasePathSchema)
    body = marshmallow.fields.Nested(IdentitySchema)


class CollectionDeleteSchema(marshmallow.Schema):
    path = marshmallow.fields.Nested(BasePathSchema)


collection_response_schemas = {
    200: IdentitySchema(exclude=["password"]),
    404: ErrorSchema()
}

collection_delete_response_schemas = {
    204: {},
    404: ErrorSchema()
}


def identity_collection_post_error_handler(request):
    response = request.response
    response.content_type = 'application/vnd.api+json'
    return response


@resource(
    collection_path="/realms/{realm_slug}/identities",
    path="/realms/{realm_slug}/identities/{id}",
    content_type="application/vnd.api+json",
    factory=IdentityContext,
)
class IdentityResource(BaseResource):

    @grip_view(schema=CollectionPostSchema, response_schema=collection_response_schemas,
               error_handler=identity_collection_post_error_handler)
    def collection_post(self):
        validated = self.request.validated["body"]

        return self.request.identity_provider.create(
            validated["username"], validated["password"], validated["name"], validated["contacts"]
        )

    def get(self):
        """ Return identity info + permissions """

        # realm = self.request.validated["path"]["realm_slug"]
        # id = self.request.validated["path"]["id"]

        # # session = AuthSession.get_session(id, realm)

        # identity = Identity.get_identity(realm, username)

        # session = AuthSession(username, password, identity)

        # return session

        # TODO: fetch permisionn
        return {}

    @grip_view(schema=CollectionDeleteSchema, response_schema=collection_delete_response_schemas)
    def delete(self):
        """Remove the identity"""

        self.request.identity_provider.delete(self.request.matchdict['id'])

        return HTTPNoContent()
