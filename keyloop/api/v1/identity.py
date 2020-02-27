import logging

import marshmallow
import marshmallow_jsonapi
from cornice.resource import resource
from pyramid.httpexceptions import HTTPAccepted, HTTPNotFound
from pyramid.security import forget, Everyone, Allow

from grip.context import SimpleBaseFactory
from grip.decorator import view as grip_view
from grip.resource import BaseResource
from keyloop.interfaces.identity import IIdentitySource, IIdentity
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


collection_response_schemas = {
    200: IdentitySchema(exclude=["password"]),
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

    @grip_view(schema=CollectionPostSchema, response_schema=collection_response_schemas, error_handler=identity_collection_post_error_handler)
    def collection_post(self):
        # where is this property being set?
        # should we define a property direct on the factory context
        validated = self.request.validated["body"]
        registry = self.request.registry.settings["keyloop_adapters"]

        identity_provider = registry.lookup([IIdentity], IIdentitySource, self.request.context.realm)

        if not identity_provider:
            self.request.errors.add(
                location='body',
                name='identity',
                description='Realm failed'
            )
            self.request.errors.status = 404
            logger.info('Realm %s is not valid.', self.request.context.realm)
            return self.request

        return identity_provider.create(
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

    def delete(self):
        """ Logout """

        # Should we trigger notifications to other services?
        forget(self.request)

        return HTTPAccepted()
