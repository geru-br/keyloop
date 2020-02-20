from freezegun import freeze_time
from pyramid.testing import DummyRequest

from keyloop.security import KeyLoopAuthenticationPolicy

import pytest


@pytest.mark.skip
def test_remember_no_realm():
    auth_p = KeyLoopAuthenticationPolicy("sekret", max_age=30)
    req = DummyRequest()
    assert auth_p.remember(req, "principal") == []


@pytest.mark.skip
def test_forget_no_realm():
    auth_p = KeyLoopAuthenticationPolicy("sekret", max_age=30)
    req = DummyRequest()
    assert auth_p.remember(req, "principal") == []


@pytest.mark.skip
@freeze_time("2020-01-14 12:00:00")
def test_remember():
    auth_p = KeyLoopAuthenticationPolicy("sekret", max_age=30)
    req = DummyRequest()
    req.realm = "clients"
    headers = auth_p.remember(req, "principal")
    cookie = (
        "ImM0NmQ4MTNlYWUyMzQwZTQ1NzUwMTczMDI0OTQyNTE2ZmY"
        "3NmQ3NmE3NTJhZDg5Y2U5MGQwNjg5OTVmOGQzMzcxMjFlZD"
        "FhMGM2MTI5NDM4N2E3NmI5NjMwODNhMTNjZjA2ZDcwMDFmO"
        "TVjZjNhNTNiZjdhZTdlNWE3YzdhNmZkcHJpbmNpcGFsIg=="
    )
    assert headers == [
        (
            "Set-Cookie",
            "kloop_clients={}; Max-Age=30; Path=/; expires=Tue, 14-Jan-2020 12:00:30 GMT".format(
                cookie
            ),
        )
    ]


@pytest.mark.skip
@freeze_time("2020-01-14 12:00:00")
def test_forget():
    auth_p = KeyLoopAuthenticationPolicy("sekret")
    req = DummyRequest()
    req.realm = "clients"
    headers = auth_p.forget(req)
    assert headers[0][0] == "Set-Cookie"
    assert "kloop_clients=;" in headers[0][1]
