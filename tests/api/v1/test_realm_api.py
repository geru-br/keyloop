from keyloop.models import DBSession
from tests.factories import RealmFactory
import pytest


def add_realm(slug, name):
    realm = RealmFactory(slug=slug, name=name)
    DBSession.add(realm)
    DBSession.flush()
    return realm


@pytest.mark.skip
def test_realm_collection_api(testapp):
    add_realm(slug="clients", name="Clients")
    add_realm(slug="admins", name="Administrators")

    res = testapp.get("/api/v1/realms")
    assert res.json == [
        {"description": "", "name": "Clients", "slug": "clients"},
        {"description": "", "name": "Administrators", "slug": "admins"},
    ]


@pytest.mark.skip
def test_realm_resource_api(testapp):
    add_realm(slug="clients", name="Clients")

    res = testapp.get("/api/v1/realms/clients")
    assert res.json == {
        "description": "",
        "name": "Clients",
        "slug": "clients",
    }


@pytest.mark.skip
def test_realm_resource_api_404(testapp):
    res = testapp.get("/api/v1/realms/clients", status=404)
    assert res.json == {
        "errors": [
            {
                "description": "Realm does not exist",
                "location": "body",
                "name": "realm_slug",
            }
        ],
        "status": "error",
    }
