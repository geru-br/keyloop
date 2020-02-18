import uuid
from unittest.mock import Mock
from http import HTTPStatus

import pytest

from tests.fake_user import DummyUser

@pytest.fixture
def login_payload():
    return {
        "data": {
            "type": "auth-session",
            "attributes": {
                "identity": {
                    "data": {
                        "type": "identity",
                        "attributes": {
                            "username": "test@test.com.br",
                            "password": "1234567a",
                        },
                    }
                }
            },
        }
    }



def test_post_auth_session_calls_registered_identity_source(pyramid_app, login_payload):

    DummyUser.test_reset()
    DummyUser.test_login_result = True
    res = pyramid_app.post_json("/api/v1/realms/REALM/auth-session", login_payload, content_type="application/vnd.api+json")

    assert res.status_code == HTTPStatus.OK
    assert res.headers["Set-Cookie"]
    assert DummyUser.test_login_called



def test_post_auth_session_fails_on_incorrect_credentials(pyramid_app, login_payload):

    DummyUser.test_reset()
    DummyUser.test_login_result = False
    res = pyramid_app.post_json("/api/v1/realms/REALM/auth-session", login_payload, content_type="application/vnd.api+json")

    assert res.status_code != HTTPStatus.OK
    # assert res.headers["Set-Cookie"]
    # assert user.get.called_once()

