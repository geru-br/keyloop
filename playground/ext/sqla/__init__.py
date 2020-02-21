from playground.ext.sqla.models import IdentitySource, ContactSource


def setup_identity(config, session, model):
    IdentitySource(session=session, model=model)

def setup_contact(config, session, model):
    ContactSource(session=session, model=model)

def includeme(config):
    config.add_directive("key_loop_setup_identity", setup_identity)
    config.add_directive("key_loop_setup_contact", setup_contact)
