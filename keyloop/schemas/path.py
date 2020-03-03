import logging

import marshmallow

from keyloop.interfaces.identity import IIdentity, IIdentitySource

logger = logging.getLogger(__name__)


class BasePathSchema(marshmallow.Schema):
    id = marshmallow.fields.UUID(required=True, dump_only=True)

    realm_slug = marshmallow.fields.String()

    @marshmallow.validates("realm_slug")
    def validate_realm(self, value):
        request = self.context["request"]
        registry = request.registry.settings["keyloop_adapters"]

        identity_provider = registry.lookup([IIdentity], IIdentitySource, value)

        if not identity_provider:
            request.errors.add(
                location='path',
                name='realm_slug',
                description='Invalid realm'
            )
            request.errors.status = 404
            logger.info('Realm %s is not valid.', request.context.realm)
            return

        request.identity_provider = identity_provider
