from keyloop.ext.sqla.auth_session import AuthSessionSource
from keyloop.ext.sqla.identity import IdentitySource
from keyloop.ext.sqla.permission import PermissionSource


def setup_models(config, session, params):
    for source_class, model in params.items():
        source_class(session=session, model=model)


def includeme(config):
    config.add_directive("keyloop_setup", setup_models)
