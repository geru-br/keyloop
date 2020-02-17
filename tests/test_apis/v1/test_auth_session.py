def test_post_auth_session(testapp):

    payload = {
        "username": "username",
        "password": "password"
    }

    res = testapp.post("/api/v1/realms/geru/auth-session", payload)
    assert True