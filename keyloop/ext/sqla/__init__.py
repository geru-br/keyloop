from keyloop.ext.sqla.identity import IdentitySource, ContactSource
from keyloop.ext.sqla.auth_session import AuthSessionSource


def setup_models(config, session, params):
    for key, value in params.items():
        merge_model = eval(key)
        merge_model(session=session, model=value)


def includeme(config):
    config.add_directive("key_loop_setup", setup_models)
