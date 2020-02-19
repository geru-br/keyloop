from wsgiref.simple_server import make_server

from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from playground.models import Base, DBSession, RealIdentity


def main():
    settings = {
        "sqlalchemy.url": "sqlite:///keyloop.dev",
        "keyloop.identity_sources": "PLAYGROUND:keyloop.ext.sqla.models.IdentitySource",
        "keyloop.authpolicysecret": "sekret",
    }

    with Configurator(settings=settings) as config:

        engine = engine_from_config(settings, "sqlalchemy.")
        DBSession.configure(bind=engine)
        Base.metadata.bind = engine

        config.include("keyloop")
        config.include("grip")
        config.include("keyloop.ext.sqla")

        config.key_loop_setup_session(DBSession, RealIdentity)

        app = config.make_wsgi_app()
    return app


if __name__ == "__main__":

    app = main()
    server = make_server("0.0.0.0", 6543, app)
    server.serve_forever()
