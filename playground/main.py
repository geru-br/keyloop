from wsgiref.simple_server import make_server

from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from keyloop.ext.sqla import IdentitySource, AuthSessionSource, PermissionSource
from playground.models import Base, DBSession, RealIdentity, RealPermission


def main():
    settings = {
        "sqlalchemy.url": "sqlite:///keyloop.dev",
        "keyloop.identity_sources": "PLAYGROUND:keyloop.ext.sqla.identity.IdentitySource",
        "keyloop.auth_session_sources": "PLAYGROUND:keyloop.ext.sqla.auth_session.AuthSessionSource",
        "keyloop.permission_sources": "PLAYGROUND:keyloop.ext.sqla.permission.PermissionSource",
        "keyloop.authpolicysecret": "sekret",
    }

    with Configurator(settings=settings) as config:
        engine = engine_from_config(settings, "sqlalchemy.")
        DBSession.configure(bind=engine)
        Base.metadata.bind = engine

        config.include("keyloop")
        config.include("grip")
        config.include("keyloop.ext.sqla")
        config.include('pyramid_tm')

        config.keyloop_setup(DBSession, {
            IdentitySource: RealIdentity,
            AuthSessionSource: RealIdentity,
            PermissionSource: RealPermission
        })

        app = config.make_wsgi_app()

    return app


if __name__ == "__main__":
    app = main()
    server = make_server("0.0.0.0", 6543, app)
    server.serve_forever()
