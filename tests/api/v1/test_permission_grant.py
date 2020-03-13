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

    def test_grant_permission_success(self, pyramid_app, perm_grant_payload, user, permission, fake_perm_grant_class):
        res = pyramid_app.post_json(f"/api/v1/realms/REALM/identities/{user.id}/permissions",
                                    perm_grant_payload,
                                    content_type="application/vnd.api+json",
                                    status=200)

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
        res = pyramid_app.post_json("/api/v1/realms/REALM/identities/9f533cff-a6b3-4430-b1b9-557da85e0121/permissions",
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
