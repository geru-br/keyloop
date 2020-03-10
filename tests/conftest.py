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
            "keyloop.perm_grant_sources": "REALM:tests.fake_permission.FakePermissionGrant",
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
def fake_user_class():
    from tests.fake_user import FakeUser
    FakeUser.test_reset()
    yield FakeUser


@pytest.fixture
def user(fake_user_class):
    user = fake_user_class.create('test@test.com.br', '1234567a')
    return user


@pytest.fixture
def fake_auth_session_class():
    from tests.fake_auth_session import FakeAuthSession
    FakeAuthSession.test_reset()
    yield FakeAuthSession


@pytest.fixture
def fake_permission_class():
    from tests.fake_permission import FakePermission
    FakePermission.test_reset()
    yield FakePermission


@pytest.fixture
def fake_perm_grant_class():
    from tests.fake_permission import FakePermissionGrant
    FakePermissionGrant.test_reset()
    yield FakePermissionGrant
