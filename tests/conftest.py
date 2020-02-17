import pytest
import transaction

from pyramid import paster
from pyramid import testing

from sqlalchemy import engine_from_config

from webtest import TestApp

from keyloop.models import DBSession
from keyloop.models.base import Base

settings = paster.get_appsettings("testing.ini", name="main")


@pytest.fixture(scope="session")
def sqlalchemy_engine():
    engine = engine_from_config(settings, "sqlalchemy.")
    DBSession.configure(bind=engine)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function", autouse=True)
def sqlalchemy_subtransaction(sqlalchemy_engine):
    connection = sqlalchemy_engine.connect()
    trans = connection.begin_nested()
    DBSession.configure(bind=connection)
    yield
    trans.rollback()
    DBSession.remove()
    transaction.abort()
    connection.close()


@pytest.fixture(scope="session")
def app():
    config = testing.setUp(settings=settings)
    yield main(config, **settings)
    testing.tearDown()


@pytest.fixture(scope="function")
def testapp(app):
    testapp_ = TestApp(
        app,
        extra_environ=dict(
            SERVER_NAME="auth.keyloop.org",
            SERVER_PORT="80",
            HTTP_HOST="auth.keyloop.org",
        ),
    )
    yield testapp_


@pytest.fixture(scope="function")
def registry(testapp):
    return testapp.app.registry
