from pyramid.config import Configurator


def main(_, **settings):
    with Configurator(settings=settings) as config:
        config.include('keyloop')
        config.include('grip')
        app = config.make_wsgi_app()
    return app