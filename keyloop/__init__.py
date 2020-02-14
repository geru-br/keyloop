from pyramid.config import Configurator
from pyramid.response import Response

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from keyloop.security import KeyLoopAuthenticationPolicy


def main(_, **settings):
    with Configurator(settings=settings) as config:
        config.include("keyloop.models")
        config.include("cornice")
        config.include('cornice_apispec')

        config.include("keyloop.api", route_prefix="/api")

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

        app = config.make_wsgi_app()
    return app
