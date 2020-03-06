import pytest
from pyramid import testing
from webtest import TestApp


@pytest.fixture(scope="session")
def pyramid_config():
    config = testing.setUp(
        settings={
            "keyloop.identity_sources": "REALM:tests.fake_user.FakeUser",
            "keyloop.auth_session_sources": "REALM:tests.fake_auth_session.FakeAuthSession",
            "keyloop.permission_sources": "REALM:tests.fake_permission.FakePermission",
            "keyloop.authpolicysecret": "sekret"
        }
    )

    config.include("keyloop")
    config.include("grip")

    return config


@pytest.fixture
def pyramid_app(pyramid_config):
    return TestApp(pyramid_config.make_wsgi_app())


@pytest.fixture
def fakeUserClass():
    from tests.fake_user import FakeUser

    FakeUser.test_reset()

    yield FakeUser


@pytest.fixture
def fakeAuthSessionClass():
    from tests.fake_auth_session import FakeAuthSession

    FakeAuthSession.test_reset()

    yield FakeAuthSession
