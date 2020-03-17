import logging

import marshmallow

from keyloop.api.v1.exceptions import IdentityNotFound
from keyloop.interfaces.auth_session import IAuthSession, IAuthSessionSource
from keyloop.interfaces.identity import IIdentity, IIdentitySource
from keyloop.interfaces.permission import IPermission, IPermissionSource

logger = logging.getLogger(__name__)


class BasePathSchema(marshmallow.Schema):
    realm_slug = marshmallow.fields.String()

    @marshmallow.validates("realm_slug")
    def validate_realm(self, value):
        request = self.context["request"]
        registry = request.registry.settings["keyloop_adapters"]

        identity_provider = registry.lookup([IIdentity], IIdentitySource, value)
        auth_session = registry.lookup([IAuthSession], IAuthSessionSource, value)
        permission_provider = registry.lookup([IPermission], IPermissionSource, value)

        if not (identity_provider or auth_session or permission_provider):
            request.errors.add(
                location='path',
                name='realm_slug',
                description='Invalid realm'
            )
            request.errors.status = 404
            logger.info('Realm %s is not valid.', request.context.realm)
            return

        request.identity_provider = identity_provider
        request.auth_session = auth_session
        request.permission_provider = permission_provider


class IdentityPathSchema(BasePathSchema):
    identity_id = marshmallow.fields.UUID()

    @marshmallow.post_load
    def validate_identity_id(self, params):
        request = self.context['request']
        try:
            identity = request.identity_provider.get(uuid=params['identity_id'])
        except IdentityNotFound:
            request.errors.add(
                location='path',
                name='identity_id',
                description='Identity not found'
            )
            request.errors.status = 404
            return

        request.identity = identity
