import sys
import pytest
from pyramid import testing
from webtest import TestApp

from unittest.mock import Mock


@pytest.fixture(scope="session")
def pyramid_config():

=======

@pytest.fixture
def pyramid_config(mock_module):
    config = testing.setUp(
        settings={

            "keyloop.identity_sources": "REALM:tests.fake_user.DummyUser",
            "keyloop.authpolicysecret": "sekret"
        }
    )

    config.include("keyloop")
    config.include("grip")

    return config


@pytest.fixture
def pyramid_app(pyramid_config):
    return TestApp(pyramid_config.make_wsgi_app())
