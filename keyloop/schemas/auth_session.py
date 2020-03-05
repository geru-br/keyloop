import marshmallow_jsonapi
import marshmallow


class BaseAuthSessionSchema(marshmallow_jsonapi.Schema):
    class Meta:
        type_ = "auth-session"

    id = marshmallow.fields.UUID(dump_only=True, attribute="uuid")
    username = marshmallow.fields.String(load_only=True)
    password = marshmallow.fields.String(load_only=True)

class AuthSessionSchema(BaseAuthSessionSchema):
    active = marshmallow.fields.Bool(dump_only=True)
    start = marshmallow.fields.DateTime(dump_only=True)
    ttl = marshmallow.fields.Integer(dump_only=True)

    identity = marshmallow_jsonapi.fields.Relationship(
        type_="identity",
        self_url='/realms/{realm_slug}/identities/{identity_id}',
        self_url_kwargs={'realm_slug': 'REALM', "identity_id": "<identity.id>"},
        schema="IdentitySchema",
        dump_only=True,
    )
