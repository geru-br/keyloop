import uuid

from unittest.mock import Mock

from http import HTTPStatus


def test_post_auth_session(pyramid_app, mock_module):
    payload = {
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

    user = Mock(
        uuid=lambda: uuid.uuid4(),
        username=lambda: "",
        password=lambda: "",
    )
    user_getter = Mock(return_value=user)
    mock_module.MockUser.get.return_value = user_getter

    res = pyramid_app.post_json("/api/v1/realms/REALM/auth-session", payload, content_type="application/vnd.api+json")

    assert res.status_code == HTTPStatus.OK
    # TODO: test if pyramid remember was called
    assert user.get.called_once()
