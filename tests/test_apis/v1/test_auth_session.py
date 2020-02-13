def test_post_auth_session(testapp):

    payload = {
        "data": {
            "type": "auth-session",
            "attributes": {
                "username": "username",
                "password": "password"
            }
        }
    }

    res = testapp.post_json("/api/v1/realms/some-realm/auth-session", payload, content_type="application/vnd.api+json", status=400)
    assert True
