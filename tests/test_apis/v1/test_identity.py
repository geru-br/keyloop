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


def test_collection_post_identity_creates_identity(pyramid_app, identity_payload):

    res = pyramid_app.post_json("/api/v1/realms/REALM/identities", identity_payload, content_type="application/vnd.api+json")
    expected_result = {
        "data": {
            "type": "identity",
            "attributes": {
                "name": "xablau",
                "username": "test@test.com",
                "contacts": [
                    {
                        "value": "11999999999",
                        "type": "MSISDN"
                    },
                    {
                        "value": "mail@mail.com",
                        "type": "EMAIL"
                    },
                ]
            }
        }
    }

    assert res.status_code == HTTPStatus.OK
    assert res.content_type == "application/vnd.api+json"
    assert sorted(res.json) == sorted(expected_result)


@pytest.mark.xfail
def test_collection_post_should_return_not_found_for_invalid_realm(pyramid_app, identity_payload):

    res = pyramid_app.post_json("/api/v1/realms/INVALID-REALM/identities",
                                identity_payload, content_type="application/vnd.api+json",
                                status=400)

    assert res.content_type == "application/vnd.api+json"
    assert res.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.xfail
def test_collection_post_should_return_bad_request_for_invalid_payload(pyramid_app, identity_payload):

    identity_payload["data"]["attributes"].pop("username")

    res = pyramid_app.post_json("/api/v1/realms/REALM/identities",
                                identity_payload, content_type="application/vnd.api+json",
                                status=400)

    assert res.content_type == "application/vnd.api+json"
    assert res.status_code == HTTPStatus.BAD_REQUEST
