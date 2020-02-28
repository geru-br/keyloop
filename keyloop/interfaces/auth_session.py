import datetime as DT
from zope.interface import (
    Interface,
    Attribute
)


class IAuthSession(Interface):
    # related_identity = Attribute('Identity uuid that is related to this session.')
    identity = Attribute('Identity that is related to this session (binded by the related_identity attrivute).')
    active = Attribute("Session's flag that indicates if it is active or not.")
    ttl = Attribute('Time that the session should be valid.')
    start = Attribute("Session's start timestamp.")


class IAuthSessionSource(Interface):
    """Marker interface for callables that retrieve an AuthSession object given it's id."""

    def get(session_id) -> IAuthSession:
        pass

    def create(related_identity: str, ttl: int, start: DT.datetime):
        pass
