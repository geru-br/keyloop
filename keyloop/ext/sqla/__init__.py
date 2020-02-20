from keyloop.ext.sqla.models import IdentitySource
import keyloop.ext.sqla.models


def setup_session(config, session, model):
    IdentitySource.session = session
    IdentitySource.model = model


def includeme(config):
    config.add_directive("key_loop_setup_session", setup_session)