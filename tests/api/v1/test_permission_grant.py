import pytest


@pytest.fixture
def permission(fake_permission_class):
    return fake_permission_class.create(name='perm_a', description='Permission for service A.')


@pytest.fixture
def perm_grant_payload():
    return {
        "data": {
            "type": "permission-grant",
            "attributes": {
                "perm_name": "perm_a",
            }
        }
    }


class TestGrantPermission:

    def test_grant_permission_success(self, pyramid_app, perm_grant_payload, user, permission):
        res = pyramid_app.post_json(f"/api/v1/realms/REALM/identities/{user.uuid}/permissions",
                                    perm_grant_payload,
                                    content_type="application/vnd.api+json",
                                    status=200)

        assert (str(permission.uuid), str(user.uuid)) in user.PERMISSION_GRANTS
        assert res.content_type == "application/vnd.api+json"
        assert res.json == {
            "data": {
                "type": "permission",
                "attributes": {
                    "description": "Permission for service A.",
                    "name": "perm_a"
                },
                "id": str(permission.uuid)
            }
        }

    def test_identity_not_found(self, pyramid_app, perm_grant_payload, user):
        inexistent_identity_id = "9f533cff-a6b3-4430-b1b9-557da85e0121"
        res = pyramid_app.post_json(f"/api/v1/realms/REALM/identities/{inexistent_identity_id}/permissions",
                                    perm_grant_payload,
                                    content_type="application/vnd.api+json",
                                    status=404)

        assert res.content_type == "application/vnd.api+json"
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

    def test_permission_not_found(self, pyramid_app, perm_grant_payload, user):
        perm_grant_payload["data"]["attributes"]["perm_name"] = "crazy-permission"
        res = pyramid_app.post_json(f"/api/v1/realms/REALM/identities/{user.uuid}/permissions",
                                    perm_grant_payload,
                                    content_type="application/vnd.api+json",
                                    status=400)

        assert res.content_type == "application/vnd.api+json"
        assert res.json == {
            "status": "error",
            "errors": [
                {
                    "location": "body",
                    "name": "perm_name",
                    "description": "Permission not found"
                }
            ]
        }

    def test_permission_already_granted_to_identity(self, pyramid_app, perm_grant_payload, user, permission):
        pyramid_app.post_json(f"/api/v1/realms/REALM/identities/{user.uuid}/permissions",
                              perm_grant_payload,
                              content_type="application/vnd.api+json",
                              status=200)

        assert {(str(permission.uuid), str(user.uuid))} == user.PERMISSION_GRANTS

        res = pyramid_app.post_json(f"/api/v1/realms/REALM/identities/{user.uuid}/permissions",
                                    perm_grant_payload,
                                    content_type="application/vnd.api+json",
                                    status=200)

        assert res.json == {
            "data": {
                "type": "permission",
                "attributes": {
                    "description": "Permission for service A.",
                    "name": "perm_a"
                },
                "id": str(permission.uuid)
            }
        }
