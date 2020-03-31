import factory

from keyloop.models import DBSession, Realm

class RealmFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Realm
        sqlalchemy_session = DBSession

    name = factory.Faker("name")
    slug = factory.LazyAttribute(lambda s: s.name.lower().replace(" ", "_"))
    description = ""
