import pytest


@pytest.fixture
def permission_payload():
    return {
        "data": {
            "type": "permission",
            "attributes": {
                "name": "permission_a",
                "description": "Permission for resource A"
            }
        }
    }


def test_create_permission(pyramid_app, permission_payload):
    res = pyramid_app.post_json("/api/v1/realms/REALM/permissions", permission_payload,
                                content_type="application/vnd.api+json",
                                status=200)

    assert res.content_type == "application/vnd.api+json"
    assert res.json == {
        "data": {
            "id": res.json['data']['id'],
            "type": "permission",
            "attributes": {
                "name": "permission_a",
                "description": "Permission for resource A"
            }
        }
    }


def test_create_permission_with_existent_name(pyramid_app, permission_payload, fake_permission_class):
    pyramid_app.post_json("/api/v1/realms/REALM/permissions", permission_payload,
                          content_type="application/vnd.api+json",
                          status=200)

    res = pyramid_app.post_json("/api/v1/realms/REALM/permissions", permission_payload,
                                content_type="application/vnd.api+json",
                                status=400)

    assert res.content_type == "application/vnd.api+json"
    assert res.json == {
        "status": "error",
        "errors": [
            {
                "location": "body",
                "name": "name",
                "description": "Existent permission with name: permission_a"
            }
        ]
    }


def test_create_permission_with_invalid_data(pyramid_app, permission_payload):
    permission_payload['data']['attributes']['description'] = ''
    res = pyramid_app.post_json("/api/v1/realms/REALM/permissions", permission_payload,
                                content_type="application/vnd.api+json",
                                status=400)

    assert res.content_type == "application/vnd.api+json"
    assert res.json == {
        "status": "error",
        "errors": [
            {
                "location": "body",
                "name": "errors",
                "description": [
                    {
                        "detail": "Invalid value.",
                        "source": {"pointer": "/data/attributes/description"}
                    }
                ]
            }
        ]
    }


def test_create_permission_with_invalid_realm(pyramid_app, permission_payload):
    res = pyramid_app.post_json("/api/v1/realms/INVALID-REALM/permissions", permission_payload,
                                content_type="application/vnd.api+json",
                                status=404)

    assert res.content_type == "application/vnd.api+json"
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


def test_get_permissions(pyramid_app, permission_payload, fake_permission_class):
    pyramid_app.post_json("/api/v1/realms/REALM/permissions", permission_payload,
                          content_type="application/vnd.api+json",
                          status=200)

    res = pyramid_app.get("/api/v1/realms/REALM/permissions", params={'page': 1, 'limit': 30})

    assert res.content_type == "application/vnd.api+json"
    assert res.json == {
        "data": [
            {
                "type": "permission",
                "attributes": {
                    "name": "permission_a",
                    "description": "Permission for resource A"
                },
                "id": res.json['data'][0]['id']
            }
        ]
    }


def test_get_permissions_empty_list(pyramid_app, permission_payload, fake_permission_class):
    pyramid_app.post_json("/api/v1/realms/REALM/permissions", permission_payload,
                          content_type="application/vnd.api+json",
                          status=200)

    res = pyramid_app.get("/api/v1/realms/REALM/permissions", params={'page': 2, 'limit': 30})

    assert res.content_type == "application/vnd.api+json"
    assert res.json == {"data": []}


def test_get_permissions_negative_page(pyramid_app, permission_payload):
    res = pyramid_app.get("/api/v1/realms/REALM/permissions", params={'page': -1, 'limit': 30}, status=400)

    assert res.content_type == "application/vnd.api+json"
    assert res.json == {
        "status": "error",
        "errors": [
            {
                "location": "querystring",
                "name": "page",
                "description": [
                    "Invalid value."
                ]
            }
        ]
    }


def test_get_permissions_negative_limit(pyramid_app, permission_payload):
    res = pyramid_app.get("/api/v1/realms/REALM/permissions", params={'page': 1, 'limit': -30}, status=400)

    assert res.content_type == "application/vnd.api+json"
    assert res.json == {
        "status": "error",
        "errors": [
            {
                "location": "querystring",
                "name": "limit",
                "description": [
                    "Invalid value."
                ]
            }
        ]
    }
