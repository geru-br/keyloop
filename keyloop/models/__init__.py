from sqlalchemy import engine_from_config

from .base import *
from .realms import *


def includeme(config):
    settings = config.registry.settings
    engine = engine_from_config(settings, "sqlalchemy.")
    DBSession.configure(bind=engine)
