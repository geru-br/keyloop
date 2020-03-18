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
        },
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
                        "detail": "Shorter than minimum length 1.",
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


def test_get_permissions_empty_list(pyramid_app, permission_payload, fake_permission_class):
    res = pyramid_app.get("/api/v1/realms/REALM/permissions", params={'page[number]': 2, 'page[size]': 30})

    assert res.content_type == "application/vnd.api+json"
    assert res.json == {
        "data": [],
        "links": {
            "self": "http://localhost/api/v1/realms/REALM/permissions?page%5Bnumber%5D=2&page%5Bsize%5D=30",
            "first": "http://localhost/api/v1/realms/REALM/permissions?page[number]=1&page[size]=30",
            "prev": "http://localhost/api/v1/realms/REALM/permissions?page[number]=1&page[size]=30",
            "next": None,
            "last": "http://localhost/api/v1/realms/REALM/permissions?page[number]=0&page[size]=30"
        },
        "meta": {
            "count": 0,
            "total_pages": 0
        }
    }


def test_get_permissions(pyramid_app, permission_payload, fake_permission_class):
    pyramid_app.post_json("/api/v1/realms/REALM/permissions", permission_payload,
                          content_type="application/vnd.api+json",
                          status=200)

    res = pyramid_app.get("/api/v1/realms/REALM/permissions", params={'page[number]': 1, 'page[size]': 30})

    permission_id = str(next(iter(fake_permission_class.PERMISSIONS.keys())))
    assert res.content_type == "application/vnd.api+json"
    assert res.json == {
        "data": [
            {
                "type": "permission",
                "attributes": {
                    "name": "permission_a",
                    "description": "Permission for resource A"
                },
                "id": permission_id
            }
        ],
        "links": {
            "self": "http://localhost/api/v1/realms/REALM/permissions?page%5Bnumber%5D=1&page%5Bsize%5D=30",
            "first": "http://localhost/api/v1/realms/REALM/permissions?page[number]=1&page[size]=30",
            "prev": None,
            "next": "http://localhost/api/v1/realms/REALM/permissions?page[number]=1&page[size]=30",
            "last": "http://localhost/api/v1/realms/REALM/permissions?page[number]=1&page[size]=30"
        },
        "meta": {
            "count": 1,
            "total_pages": 1
        }
    }


def test_get_permissions_negative_page(pyramid_app, permission_payload):
    res = pyramid_app.get("/api/v1/realms/REALM/permissions", params={'page[number]': -1, 'page[size]': 30}, status=400)

    assert res.content_type == "application/vnd.api+json"
    assert res.json == {
        "status": "error",
        "errors": [
            {
                "location": "querystring",
                "name": "page[number]",
                "description": [
                    "Invalid value."
                ]
            }
        ]
    }


def test_get_permissions_negative_limit(pyramid_app, permission_payload):
    res = pyramid_app.get("/api/v1/realms/REALM/permissions", params={'page[number]': 1, 'page[size]': -30}, status=400)

    assert res.content_type == "application/vnd.api+json"
    assert res.json == {
        "status": "error",
        "errors": [
            {
                "location": "querystring",
                "name": "page[size]",
                "description": [
                    "Invalid value."
                ]
            }
        ]
    }
