from datetime import datetime

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
        pyramid_app, login_payload, user
):
    with freeze_time(datetime.utcnow()):
        res = pyramid_app.post_json(
            "/api/v1/realms/REALM/auth-session",
            login_payload,
            content_type="application/vnd.api+json",
            status=200,
        )

        # TODO: check the returned cookie to assert that it checks with the current session id
        assert "Set-Cookie" in res.headers

        expected_result = {
            "data": {
                "type": "auth-session",
                "attributes": {
                    'active': True,
                    'start': arrow.utcnow().datetime.isoformat(),
                    'ttl': 600
                },
                "id": res.json['data']['id'],
                "relationships": {
                    "identity": {
                        "links": {
                            "self": f"/realms/REALM/identities/{str(user.uuid)}"
                        },
                        "data": {
                            "type": "identity",
                            "id": str(user.uuid)
                        }
                    }
                }
            },
            "included": [
                {
                    "type": "identity",
                    "id": str(user.uuid),
                    "attributes": {
                        "name": None,
                        "username": "test@test.com.br",
                        'active': True,
                        "permissions": ['perm_a', 'perm_b', 'perm_c']
                    }
                }
            ]
        }

        assert res.json == expected_result


def test_post_auth_session_fails_on_non_existing_realm(
        pyramid_app, login_payload, fake_user_class
):
    fake_user_class.test_login_result = False

    res = pyramid_app.post_json(
        "/api/v1/realms/WRONGREALM/auth-session",
        login_payload,
        content_type="application/vnd.api+json",
        status=404,
    )

    assert "Set-Cookie" not in res.headers


def test_post_auth_session_fails_on_non_existing_user(
        pyramid_app, login_payload, fake_user_class
):
    fake_user_class.test_login_result = False
    login_payload["data"]["attributes"]["username"] = "wrongusername"

    res = pyramid_app.post_json(
        "/api/v1/realms/REALM/auth-session",
        login_payload,
        content_type="application/vnd.api+json",
        status=404,
    )
    assert res.content_type == "application/vnd.api+json"
    assert "Set-Cookie" not in res.headers


def test_post_auth_session_fails_on_incorrect_credentials(
        pyramid_app, login_payload, fake_user_class, user
):
    fake_user_class.test_login_result = False
    login_payload["data"]["attributes"]["password"] = "wrongpassword"

    res = pyramid_app.post_json(
        "/api/v1/realms/REALM/auth-session",
        login_payload,
        content_type="application/vnd.api+json",
        status=401,
    )

    assert res.content_type == "application/vnd.api+json"
    assert "Set-Cookie" not in res.headers


def test_get_auth_session(
        pyramid_app, login_payload, fake_user_class, user
):
    pyramid_app.post_json(
        "/api/v1/realms/REALM/auth-session",
        login_payload,
        content_type="application/vnd.api+json",
        status=200,
    )

    res = pyramid_app.get("/api/v1/realms/REALM/auth-session")
    assert res.content_type == "application/vnd.api+json"


def test_get_auth_session_wrong_realm(
        pyramid_app, login_payload, fake_user_class, user
):
    pyramid_app.post_json(
        "/api/v1/realms/REALM/auth-session",
        login_payload,
        content_type="application/vnd.api+json",
        status=200,
    )

    res = pyramid_app.get("/api/v1/realms/WRONGREALM/auth-session", status=404)
    assert res.content_type == "application/vnd.api+json"


def test_get_auth_session_not_found(
        pyramid_app, login_payload, fake_user_class
):
    res = pyramid_app.get("/api/v1/realms/REALM/auth-session", status=404)
    assert res.content_type == "application/vnd.api+json"
    assert res.json == {
        "status": "error",
        "errors": [
            {
                "location": "header",
                "name": "retrieve_auth_session",
                "description": "Auth session not found"
            }
        ]
    }


def test_delete_auth_session(
        pyramid_app, login_payload, fake_user_class, fake_auth_session_class, user
):
    res = pyramid_app.post_json(
        "/api/v1/realms/REALM/auth-session",
        login_payload,
        content_type="application/vnd.api+json",
        status=200,
    )

    identity_id = res.json['data']['relationships']['identity']['data']['id']
    assert "Set-Cookie" in res.headers

    res = pyramid_app.delete_json(
        "/api/v1/realms/REALM/auth-session/{}".format(identity_id),
        content_type="application/vnd.api+json",
        status=204
    )
    assert "Set-Cookie" not in res.headers
