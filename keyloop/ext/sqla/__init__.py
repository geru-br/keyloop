from keyloop.ext.sqla.models import IdentitySource
import keyloop.ext.sqla.models


def setup_session(config, session, model):
    # Instantiates singleton class with the needed attrs
    IdentitySource(session=session, model=model)


def includeme(config):
    config.add_directive("key_loop_setup_session", setup_session)
