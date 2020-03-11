from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from playground.models import Base, DBSession, RealIdentity


def main(_, **settings):
    with Configurator(settings=settings) as config:
        engine = engine_from_config(settings, "sqlalchemy.")
        DBSession.configure(bind=engine)
        Base.metadata.bind = engine

        config.include("keyloop")
        config.include("grip")
        config.include("keyloop.ext.sqla")
        config.include('pyramid_tm')

        config.key_loop_setup(DBSession, {
            'IdentitySource': RealIdentity,
            'AuthSessionSource': RealIdentity
        })

        app = config.make_wsgi_app()
    return app
