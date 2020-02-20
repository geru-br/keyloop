import transaction

from keyloop.models import DBSession, Realm
from tests.factories import RealmFactory

import pytest


@pytest.mark.skip
def test_realm_config():
    blog = RealmFactory(slug="blog", name="Blog")
    transaction.commit()
    DBSession.add(blog)

    realm = Realm.query.filter_by(uuid=blog.uuid).first()
    assert realm.name == "Blog"
