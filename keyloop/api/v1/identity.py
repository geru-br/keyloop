import marshmallow
from cornice.resource import resource
from pyramid.httpexceptions import HTTPAccepted, HTTPUnauthorized, HTTPNotFound
from pyramid.config import Configurator
from pyramid.security import remember, forget, Everyone, Allow
from zope.interface.adapter import AdapterRegistry

from grip.context import SimpleBaseFactory
from grip.resource import BaseResource
from keyloop.interfaces.identity import IIdentitySource, IIdentity
from keyloop.schemas.identity import IdentitySchema
from keyloop.schemas.path import BasePathSchema

import logging

logger = logging.getLogger(__name__)


class IdentityContext(SimpleBaseFactory):
    def __acl__(self):
        # TODO: implement access permission (fixed token?)
        return [(Allow, Everyone, 'edit')]


class CollectionPostSchema(marshmallow.Schema):
    path = marshmallow.fields.Nested(BasePathSchema)
    body = marshmallow.fields.Nested(IdentitySchema)


collection_response_schemas = {200: IdentitySchema(exclude=["password"])}


@resource(
    collection_path="/realms/{realm_slug}/identities",
    path="/realms/{realm_slug}/identities/{id}",
    content_type="application/vnd.api+json",
    factory=IdentityContext,
)
class IdentityResource(BaseResource):
    collection_post_schema = CollectionPostSchema
    collection_response_schemas = collection_response_schemas

    def collection_post(self):
        # where is this property being set?
        # should we define a property direct on the factory context

        validated = self.request.validated["body"]

        username = validated["username"]
        password = validated["password"]
        name = validated["name"]
        contacts = validated["contacts"]

        registry = self.request.registry.settings["keyloop_adapters"]

        identity_provider = registry.lookup([IIdentity], IIdentitySource, self.context.realm)

        if not identity_provider:
            # realm not found
            raise HTTPNotFound("No such realm")

        try:
            identity = identity_provider.create(username, password, name, contacts)
            return identity
        except Exception as e:
            logger.error("Could not create new Identity: '%s'", e)
            raise

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
