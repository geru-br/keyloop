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
            }
        }
    }


def test_collection_post_identity_creates_identity(pyramid_app, identity_payload, fake_user_class):
    res = pyramid_app.post_json("/api/v1/realms/REALM/identities", identity_payload,
                                content_type="application/vnd.api+json", status=200, )
    expected_result = {
        "data": {
            "type": "identity",
            "attributes": {
                "username": "test@test.com",
                'active': True,
                "name": "xablau"
            }
        }
    }

    expected_result['data']['id'] = res.json['data']['id']

    assert res.content_type == "application/vnd.api+json"
    assert res.json == expected_result


def test_collection_post_nonexistent_realm(pyramid_app, identity_payload, fake_user_class):
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


def test_collection_post_invalid_payload(pyramid_app, identity_payload, fake_user_class):
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


def test_delete_identity(pyramid_app, identity_payload, fake_user_class):
    pyramid_app.post_json("/api/v1/realms/REALM/identities", identity_payload,
                          content_type="application/vnd.api+json", status=200, )

    id = str(next(iter(fake_user_class.IDENTITIES.keys())))
    assert fake_user_class.IDENTITIES[id]['active'] is True

    pyramid_app.delete_json("/api/v1/realms/REALM/identities/{}".format(id),
                            content_type="application/vnd.api+json",
                            status=204)

    assert fake_user_class.IDENTITIES[id]['active'] is False


def test_delete_identity_not_found(pyramid_app, identity_payload, fake_user_class):
    pyramid_app.post_json("/api/v1/realms/REALM/identities", identity_payload,
                          content_type="application/vnd.api+json", status=200, )

    assert len(fake_user_class.IDENTITIES) == 1

    res = pyramid_app.delete_json("/api/v1/realms/REALM/identities/49a22924-cfa5-45e8-8f8f-7933426b6d68",
                                  content_type="application/vnd.api+json",
                                  status=404)

    assert len(fake_user_class.IDENTITIES) == 1
    assert res.json == {
        "status": "error",
        "errors": [
            {
                "location": "path",
                "name": "identity_id",
                "description": "Identity not found"
            }
        ]
    }


def test_get_identity(pyramid_app, fake_user_class, user):
    res = pyramid_app.get(f"/api/v1/realms/REALM/identities/{user.id}", status=200)

    assert res.json == {
        "data": {
            "type": "identity",
            "attributes": {
                "permissions": [
                    "perm_a",
                    "perm_b",
                    "perm_c"
                ],
                "name": None,
                'active': True,
                "username": "test@test.com.br"
            },
            "id": str(user.id)
        }
    }


def test_update_identity(pyramid_app, identity_payload, fake_user_class):
    res = pyramid_app.post_json("/api/v1/realms/REALM/identities", identity_payload,
                                content_type="application/vnd.api+json", status=200, )

    assert identity_payload['data']['attributes']['name'] == res.json['data']['attributes']['name']

    identity_payload["data"]["attributes"]["name"] = "updated user"
    identity_payload["data"]["attributes"].pop("username")

    identity_id = str(next(iter(fake_user_class.IDENTITIES.keys())))
    pyramid_app.patch_json(f"/api/v1/realms/REALM/identities/{identity_id}",
                           identity_payload,
                           content_type="application/vnd.api+json", status=204, )

    assert fake_user_class.IDENTITIES[identity_id]['name'] == \
           identity_payload["data"]["attributes"]["name"]


def test_update_error_identity(pyramid_app, identity_payload, fake_user_class):
    res = pyramid_app.post_json("/api/v1/realms/REALM/identities", identity_payload,
                                content_type="application/vnd.api+json", status=200, )

    assert identity_payload['data']['attributes']['name'] == res.json['data']['attributes']['name']

    identity_payload["data"]["attributes"]["name"] = "updated user"
    updated_identity = pyramid_app.patch_json("/api/v1/realms/REALM/identities/49a22924-cfa5-45e8-8f8f-7933426b6d68",
                                              identity_payload,
                                              content_type="application/vnd.api+json",
                                              status=404)

    assert updated_identity.json == {
        "status": "error",
        "errors": [
            {
                "location": "path",
                "name": "identity_id",
                "description": "Identity not found"
            }
        ]
    }


def test_update_identity_password(pyramid_app, identity_payload, fake_user_class):
    pyramid_app.post_json("/api/v1/realms/REALM/identities", identity_payload,
                          content_type="application/vnd.api+json", status=200, )

    params = {
        "data": {
            "type": "identity",
            "attributes": {
                "last_password": identity_payload["data"]["attributes"]["password"],
                "password": "123456a",
            }
        }
    }

    identity_id = str(next(iter(fake_user_class.IDENTITIES.keys())))
    pyramid_app.patch_json(f"/api/v1/realms/REALM/identities/{identity_id}/password",
                           params,
                           content_type="application/vnd.api+json", status=204, )

    assert fake_user_class.IDENTITIES[identity_id]['password'] == params["data"]["attributes"]["password"]


def test_update_identity_password_user_not_found(pyramid_app, identity_payload, fake_user_class):
    pyramid_app.post_json("/api/v1/realms/REALM/identities", identity_payload,
                          content_type="application/vnd.api+json", status=200, )

    params = {
        "data": {
            "type": "identity",
            "attributes": {
                "last_password": identity_payload["data"]["attributes"]["password"],
                "password": "123456a",
            }
        }
    }

    res = pyramid_app.patch_json("/api/v1/realms/REALM/identities/49a22924-cfa5-45e8-8f8f-7933426b6d68/password",
                                 params,
                                 content_type="application/vnd.api+json", status=404, )

    assert res.json == {
        "status": "error",
        "errors": [
            {
                "location": "path",
                "name": "identity_id",
                "description": "Identity not found"
            }
        ]
    }


def test_update_identity_password_authentication_failed(pyramid_app, identity_payload, fake_user_class):
    pyramid_app.post_json("/api/v1/realms/REALM/identities", identity_payload,
                          content_type="application/vnd.api+json", status=200, )

    params = {
        "data": {
            "type": "identity",
            "attributes": {
                "last_password": "wrongpassword",
                "password": "123456a",
            }
        }
    }

    identity_id = str(next(iter(fake_user_class.IDENTITIES.keys())))
    res = pyramid_app.patch_json(f"/api/v1/realms/REALM/identities/{identity_id}/password",
                                 params,
                                 content_type="application/vnd.api+json", status=401, )

    assert res.json == {
        "status": "error",
        "errors": [
            {
                "location": "body",
                "name": "last_password",
                "description": "Last password not match"
            }
        ]
    }
