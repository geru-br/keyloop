import sys
import pytest
from pyramid import testing
from webtest import TestApp

from unittest.mock import Mock

PY3K = sys.version_info >= (3, 0)

#@pytest.fixture
#def mock_module():
    #"""Creates a fake "testing_mock" module
    #that can be "imported" by parts of the app being tested.

    #The classes that are intended to be tested (if they are instantiated/methods calles, etc),
    #are created as permanent attributes on the fake module (Currently only MockUser)


    #"""
    #import sys
    #if not "testing_mock" in sys.modules:
        #sys.modules["testing_mock"] = Mock()

    #TestingModule = sys.modules["testing_mock"]
    #TestingModule.MockUser.reset_mock()
    #return TestingModule

@pytest.fixture(scope="session")
def pyramid_config():

    config = testing.setUp(
        settings={

            "keyloop.identity_sources": "REALM:tests.fake_user.FakeUser",
            "keyloop.authpolicysecret": "sekret"
        }
    )

    config.include("keyloop")
    config.include("grip")
    # config.scan('.')

    return config


@pytest.fixture
def pyramid_app(pyramid_config):
    return TestApp(pyramid_config.make_wsgi_app())


