import logging

from zope.interface.adapter import AdapterRegistry

from pyramid.settings import aslist

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy


from keyloop.interfaces import auth_session, identity

logger = logging.getLogger(__name__)


def _register_adapters(config):
    settings = config.registry.settings
    adapter_registry = AdapterRegistry()

    list_of_identity_adapters = aslist(settings["keyloop.identity_sources"])
    for adapter_description in list_of_identity_adapters:
        realm, identity_source_name = adapter_description.split(":")

        adapter_registry.register(
            [identity.IIdentity],
            identity.IIdentitySource,
            realm,
            config.maybe_dotted(identity_source_name)
        )

    list_of_auth_session_adapters = aslist(settings["keyloop.auth_session_sources"])
    for adapter_description in list_of_auth_session_adapters:
        realm, auth_session_source_name = adapter_description.split(":")

        logger.debug("Registered IIdentitySource adapter for realm '%s'", realm)
        adapter_registry.register(
            [auth_session.IAuthSession],
            auth_session.IAuthSessionSource,
            realm,
            config.maybe_dotted(auth_session_source_name)
        )

    config.registry.settings["keyloop_adapters"] = adapter_registry


def includeme(config):
    config.include("cornice")
    config.include('cornice_apispec')

    config.include("keyloop.api.v1", route_prefix="/api/v1")

    # Security policies
    authn_policy = AuthTktAuthenticationPolicy(
        config.registry.settings["keyloop.authpolicysecret"],
        max_age=30,
        # hashalg="sha512",
        # wild_domain=False,
        # domain=".geru-local.com.br"
        # callback=groupfinder,
    )
    authz_policy = ACLAuthorizationPolicy()
    config.set_authorization_policy(authz_policy)
    config.set_authentication_policy(authn_policy)
    _register_adapters(config)

    config.scan(ignore=['keyloop.api.v1'])
