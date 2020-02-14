from pyramid.config import Configurator
from pyramid.response import Response

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from grip.renderers import json_api_renderer

from keyloop.security import KeyLoopAuthenticationPolicy


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

    config.scan(ignore=['keyloop.api.v1'])
