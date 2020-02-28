from datetime import datetime
from http import HTTPStatus
import arrow
import pytest
from freezegun import freeze_time


@pytest.fixture
def login_payload():
    return {
        "data": {
            "type": "auth-session",
            "attributes": {
                "username": "test@test.com.br",
                "password": "1234567a"
            }
        }
    }


def test_post_auth_session_calls_registered_identity_source(
    pyramid_app, login_payload, fakeUserClass
):

    with freeze_time(datetime.utcnow()):
        res = pyramid_app.post_json(
            "/api/v1/realms/REALM/auth-session",
            login_payload,
            content_type="application/vnd.api+json",
        )

        assert res.status_code == HTTPStatus.OK
        # TODO: check the returned cookie to assert that it checks with the current session id
        assert "Set-Cookie" in res.headers
        assert fakeUserClass.test_login_called
        # FIXME: We must return identity data at the same request

        expected_result = {
            "data": {
                "type": "auth-session",
                "attributes": {
                    'active': True,
                    'start': arrow.utcnow().datetime.isoformat(),
                    'ttl': 600
                },
                "relationships": {
                    "identity": {
                        "links": {
                            "self": "/realms/REALM/identities/1bed6e99-74d8-484a-a650-fab8f4f80506"
                        },
                        "data": {
                            "type": "identity",
                            "id": "1bed6e99-74d8-484a-a650-fab8f4f80506"
                        }
                    }
                }
            },
            "included": [
                {
                    "type": "identity",
                    "id": "1bed6e99-74d8-484a-a650-fab8f4f80506",
                    "attributes": {
                        "name": None,
                        "username": "test@test.com.br",
                        "contacts": None
                    }
                }
            ]
        }

        assert res.json == expected_result


def test_post_auth_session_fails_on_non_existing_user(
    pyramid_app, login_payload, fakeUserClass
):

    fakeUserClass.test_login_result = False
    login_payload["data"]["attributes"]["username"] = "wrongusername"

    res = pyramid_app.post_json(
        "/api/v1/realms/REALM/auth-session",
        login_payload,
        content_type="application/vnd.api+json",
        status=400,
    )
    assert res.status_code == HTTPStatus.BAD_REQUEST
    assert "Set-Cookie" not in res.headers


def test_post_auth_session_fails_on_incorrect_credentials(
    pyramid_app, login_payload, fakeUserClass
):

    fakeUserClass.test_login_result = False
    login_payload["data"]["attributes"]["password"] = "wrongpassword"

    res = pyramid_app.post_json(
        "/api/v1/realms/REALM/auth-session",
        login_payload,
        content_type="application/vnd.api+json",
        status=400,
    )

    assert res.status_code == HTTPStatus.BAD_REQUEST
    assert "Set-Cookie" not in res.headers


def test_get_auth_session(
    pyramid_app, login_payload, fakeUserClass
):
    res = pyramid_app.post_json(
        "/api/v1/realms/REALM/auth-session",
        login_payload,
        content_type="application/vnd.api+json",
    )

    identity_id = res.json['data']['relationships']['identity']['data']['id']

    res = pyramid_app.get(
        "/api/v1/realms/REALM/auth-session/{}".format(identity_id), status=200
    )
    assert res.content_type == "application/vnd.api+json"
    assert res.status_code == HTTPStatus.OK


def test_delete_auth_session(
    pyramid_app, login_payload, fakeUserClass, fakeAuthSessionClass
):
    res = pyramid_app.post_json(
        "/api/v1/realms/REALM/auth-session",
        login_payload,
        content_type="application/vnd.api+json",
    )

    identity_id = res.json['data']['relationships']['identity']['data']['id']

    res = pyramid_app.delete_json(
        "/api/v1/realms/REALM/auth-session/{}".format(identity_id), content_type="application/vnd.api+json", status=200
    )
    assert res.content_type == "application/vnd.api+json"
    assert res.status_code == HTTPStatus.OK
    assert fakeAuthSessionClass.test_delete_called == True
