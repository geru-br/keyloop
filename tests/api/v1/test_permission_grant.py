import pytest


@pytest.fixture
def identity(fake_user_class):
    return fake_user_class.create('test@test.com.br', '1234567a', 'Test', [])


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


def test_create_permission_grant(pyramid_app, perm_grant_payload, identity, permission, fake_perm_grant_class):
    res = pyramid_app.post_json(f"/api/v1/realms/REALM/identities/{identity.id}/permissions",
                                perm_grant_payload,
                                content_type="application/vnd.api+json",
                                status=200)

    assert res.content_type == "application/vnd.api+json"
    assert res.json == {
        "data": {
            "type": "permission-grant",
            "id": str(next(iter(fake_perm_grant_class.PERMISSION_GRANTS)))
        }
    }
