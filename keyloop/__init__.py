from zope.interface.adapter import AdapterRegistry

from pyramid.config import Configurator
from pyramid.response import Response

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from grip.renderers import json_api_renderer

from keyloop.security import KeyLoopAuthenticationPolicy

from keyloop.interfaces import identity


def _register_adapters(config):
    settings = config.registry.settings
    adapter_registry = AdapterRegistry()

    realm, identity_source_name = settings["keyloop.identity_source"].split(":")

    adapter_registry.register([identity.IIdentitySource], identity.IIdentity, realm,
                              config.maybe_dotted(identity_source_name))

    config.registry.settings["keyloop_adapters"] = adapter_registry


def includeme(config):
    config.include("cornice")
    config.include('cornice_apispec')

    config.include("keyloop.api.v1", route_prefix="/api/v1")

    # Security policies
    authn_policy = KeyLoopAuthenticationPolicy(
        "sekret",
        max_age=30,
        # hashalg="sha512",
        # wild_domain=False,
        # domain=".geru-local.com.br"
        # callback=groupfinder,
    )
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    _register_adapters(config)

    config.scan(ignore=['keyloop.api.v1'])
