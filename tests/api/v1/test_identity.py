from http import HTTPStatus

import pytest


@pytest.fixture
def identity_payload():
    return {
        "data": {
            "type": "identity",
            "attributes": {
                "username": "test@test.com",
                "password": "blablabla",
                "name": "xablau",
                "contacts": [
                    {
                        "type": "EMAIL",
                        "value": "mail@mail.com",
                    },
                    {
                        "type": "MSISDN",
                        "value": "11999999999",
                    },
                ]
            }
        }
    }


def test_collection_post_identity_creates_identity(pyramid_app, identity_payload, fakeUserClass):
    res = pyramid_app.post_json("/api/v1/realms/REALM/identities", identity_payload,
                                content_type="application/vnd.api+json")
    expected_result = {
        "data": {
            "type": "identity",
            "attributes": {
                "username": "test@test.com",
                "contacts": [
                    {
                        "type": "EMAIL",
                        "value": "mail@mail.com"
                    },
                    {
                        "type": "MSISDN",
                        "value": "11999999999"
                    }
                ],
                "name": "xablau"
            }
        }
    }

    expected_result['data']['id'] = res.json['data']['id']

    assert res.status_code == HTTPStatus.OK
    assert res.content_type == "application/vnd.api+json"
    assert res.json == expected_result


@pytest.mark.xfail(reason="res.content_type should be application/vnd.api+json")
def test_collection_post_nonexistent_realm(pyramid_app, identity_payload, fakeUserClass):
    res = pyramid_app.post_json("/api/v1/realms/INVALID-REALM/identities",
                                identity_payload, content_type="application/vnd.api+json",
                                status=404)

    assert res.json == {
        "status": "error",
        "errors": [
            {
                "location": "path",
                "name": "realm_slug",
                "description": "Invalid realm"
            }
        ]
    }
    assert res.content_type == "application/vnd.api+json"


@pytest.mark.xfail(reason="res.content_type should be application/vnd.api+json")
def test_collection_post_invalid_payload(pyramid_app, identity_payload, fakeUserClass):
    import copy
    local_identity_payload = copy.deepcopy(identity_payload)
    local_identity_payload["data"]["attributes"].pop("username")

    res = pyramid_app.post_json("/api/v1/realms/REALM/identities",
                                local_identity_payload, content_type="application/vnd.api+json",
                                status=400)

    assert res.json == {
        "status": "error",
        "errors": [
            {
                "location": "body",
                "name": "errors",
                "description": [
                    {
                        "detail": "Missing data for required field.",
                        "source": {
                            "pointer": "/data/attributes/username"
                        }
                    }
                ]
            }
        ]
    }
    assert res.content_type == "application/vnd.api+json"


def test_delete_identity(pyramid_app, fakeUserClass):
    res = pyramid_app.delete_json("/api/v1/realms/REALM/identities/2", content_type="application/vnd.api+json",
                                  status=204)

    assert res.status_code == HTTPStatus.NO_CONTENT
    assert fakeUserClass.test_delete_called


def test_get_identity(pyramid_app, fakeUserClass):
    res = pyramid_app.get("/api/v1/realms/REALM/identities/d298694ccf6a496e95f9f4a4835e69a2", status=200)

    assert res.json == {
        "data": {
            "type": "identity",
            "attributes": {
                "permissions": [
                    "perm_a",
                    "perm_b",
                    "perm_c"
                ],
                "contacts": None,
                "name": None,
                "username": "teste@email.com.br"
            },
            "id": "d298694c-cf6a-496e-95f9-f4a4835e69a2"
        }
    }


def test_update_identity(pyramid_app, identity_payload, fakeUserClass):
    res = pyramid_app.post_json("/api/v1/realms/REALM/identities", identity_payload,
                                content_type="application/vnd.api+json")

    assert identity_payload['data']['attributes']['name'] == res.json['data']['attributes']['name']

    import copy
    local_identity_payload = copy.deepcopy(identity_payload)
    local_identity_payload["data"]["attributes"]["name"] = "updated user"

    updated_identity = pyramid_app.put_json("/api/v1/realms/REALM/identities/2", local_identity_payload,
                                            content_type="application/vnd.api+json")

    assert updated_identity.status_code == HTTPStatus.NO_CONTENT
    assert fakeUserClass.IDENTITIES[0]['name'] == local_identity_payload["data"]["attributes"]["name"]


def test_update_error_identity(pyramid_app, identity_payload, fakeUserClass):
    res = pyramid_app.post_json("/api/v1/realms/REALM/identities", identity_payload,
                                content_type="application/vnd.api+json")

    assert identity_payload['data']['attributes']['name'] == res.json['data']['attributes']['name']

    import copy
    local_identity_payload = copy.deepcopy(identity_payload)
    local_identity_payload["data"]["attributes"]["name"] = "updated user"
    updated_identity = pyramid_app.put_json("/api/v1/realms/REALM/identities/1",
                                            local_identity_payload,
                                            content_type="application/vnd.api+json",
                                            status=404)

    assert fakeUserClass.IDENTITIES[0]['name'] != local_identity_payload["data"]["attributes"]["name"]
    assert updated_identity.json == {
        "status": "error",
        "errors": [
            {
                "location": "path",
                "name": "identity_update",
                "description": "Identity not found"
            }
        ]
    }
