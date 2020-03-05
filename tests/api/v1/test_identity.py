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

    assert res.content_type == "application/vnd.api+json"
    assert res.json == expected_result


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


def test_collection_post_invalid_payload(pyramid_app, identity_payload, fakeUserClass):
    identity_payload["data"]["attributes"].pop("username")

    res = pyramid_app.post_json("/api/v1/realms/REALM/identities",
                                identity_payload, content_type="application/vnd.api+json",
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


def test_delete_identity(pyramid_app, identity_payload, fakeUserClass):
    pyramid_app.post_json("/api/v1/realms/REALM/identities", identity_payload,
                          content_type="application/vnd.api+json")

    assert len(fakeUserClass.IDENTITIES) == 1

    pyramid_app.delete_json("/api/v1/realms/REALM/identities/1bed6e99-74d8-484a-a650-fab8f4f80506",
                            content_type="application/vnd.api+json",
                            status=204)

    assert len(fakeUserClass.IDENTITIES) == 0


def test_delete_identity_not_found(pyramid_app, identity_payload, fakeUserClass):
    pyramid_app.post_json("/api/v1/realms/REALM/identities", identity_payload,
                          content_type="application/vnd.api+json")

    assert len(fakeUserClass.IDENTITIES) == 1

    res = pyramid_app.delete_json("/api/v1/realms/REALM/identities/49a22924-cfa5-45e8-8f8f-7933426b6d68",
                                  content_type="application/vnd.api+json",
                                  status=404)

    assert len(fakeUserClass.IDENTITIES) == 1
    assert res.json == {
        "status": "error",
        "errors": [
            {
                "location": "path",
                "name": "identity_delete",
                "description": "Identity not found"
            }
        ]
    }


def test_get_identity(pyramid_app, fakeUserClass):
    res = pyramid_app.get("/api/v1/realms/REALM/identities/1bed6e9974d8484aa650fab8f4f80506", status=200)

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
                "username": "test@test.com.br"
            },
            "id": "1bed6e99-74d8-484a-a650-fab8f4f80506"
        }
    }


def test_update_identity(pyramid_app, identity_payload, fakeUserClass):
    res = pyramid_app.post_json("/api/v1/realms/REALM/identities", identity_payload,
                                content_type="application/vnd.api+json")

    assert identity_payload['data']['attributes']['name'] == res.json['data']['attributes']['name']

    identity_payload["data"]["attributes"]["name"] = "updated user"
    identity_payload["data"]["attributes"].pop("username")

    pyramid_app.put_json("/api/v1/realms/REALM/identities/1bed6e99-74d8-484a-a650-fab8f4f80506",
                         identity_payload,
                         content_type="application/vnd.api+json")

    assert fakeUserClass.IDENTITIES['1bed6e99-74d8-484a-a650-fab8f4f80506']['name'] == \
           identity_payload["data"]["attributes"]["name"]


def test_update_error_identity(pyramid_app, identity_payload, fakeUserClass):
    res = pyramid_app.post_json("/api/v1/realms/REALM/identities", identity_payload,
                                content_type="application/vnd.api+json")

    assert identity_payload['data']['attributes']['name'] == res.json['data']['attributes']['name']

    identity_payload["data"]["attributes"]["name"] = "updated user"
    updated_identity = pyramid_app.put_json("/api/v1/realms/REALM/identities/49a22924-cfa5-45e8-8f8f-7933426b6d68",
                                            identity_payload,
                                            content_type="application/vnd.api+json",
                                            status=404)

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
