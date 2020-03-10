import logging

import marshmallow

from keyloop.interfaces.auth_session import IAuthSession, IAuthSessionSource
from keyloop.interfaces.identity import IIdentity, IIdentitySource
from keyloop.interfaces.permission import IPermission, IPermissionSource
from keyloop.interfaces.permission_grant import IPermissionGrant, IPermissionGrantSource

logger = logging.getLogger(__name__)


class BasePathSchema(marshmallow.Schema):
    id = marshmallow.fields.UUID()

    realm_slug = marshmallow.fields.String()

    @marshmallow.validates("realm_slug")
    def validate_realm(self, value):
        request = self.context["request"]
        registry = request.registry.settings["keyloop_adapters"]

        identity_provider = registry.lookup([IIdentity], IIdentitySource, value)
        auth_session = registry.lookup([IAuthSession], IAuthSessionSource, value)
        permission_provider = registry.lookup([IPermission], IPermissionSource, value)
        perm_grant_provider = registry.lookup([IPermissionGrant], IPermissionGrantSource, value)

        if not (identity_provider or auth_session or permission_provider or perm_grant_provider):
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
        request.perm_grant_provider = perm_grant_provider


class PermissionGrantPathSchema(BasePathSchema):
    perm_grant_id = marshmallow.fields.UUID()
