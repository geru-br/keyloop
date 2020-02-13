def test_post_auth_session(testapp):

    payload = {
        "data": {
            "type": "auth-session",
            "attributes": {
                "username": "username",
                "password": "blablabla"
            }
        }
    }

    res = testapp.post_json("/api/v1/realms/some-realm/auth-session", payload, content_type="application/vnd.api+json")
    assert True
