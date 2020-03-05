import datetime as DT
from zope.interface import (
    Interface,
    Attribute
)


class IAuthSession(Interface):
    identity = Attribute('Identity that is related to this session (binded by the related_identity attrivute).')
    active = Attribute("Session's flag that indicates if it is active or not.")
    ttl = Attribute('Time that the session should be valid.')
    start = Attribute("Session's start timestamp.")



class IAuthSessionSource(Interface):
    """Marker interface for callables that retrieve an AuthSession object given it's id."""

    def get(session_id) -> IAuthSession:
        pass

    def delete(self):
        pass

    def login(username, password):
        pass
