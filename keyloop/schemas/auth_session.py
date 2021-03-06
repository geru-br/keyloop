import marshmallow_jsonapi
import marshmallow


class AuthSessionSchema(marshmallow_jsonapi.Schema):
    class Meta:
        type_ = "auth-session"

    id = marshmallow.fields.UUID(dump_only=True, attribute="uuid")
    username = marshmallow.fields.String(required=True, load_only=True)
    password = marshmallow.fields.String(required=True, load_only=True)
    active = marshmallow.fields.Bool(dump_only=True)
    start = marshmallow.fields.DateTime(dump_only=True)
    ttl = marshmallow.fields.Integer(dump_only=True)
    identity = marshmallow_jsonapi.fields.Relationship(
        type_="identity",
        self_url='/realms/{realm_slug}/identities/{identity_id}',
        self_url_kwargs={'realm_slug': 'REALM', "identity_id": "<identity.uuid>"},
        schema="IdentitySchema",
        dump_only=True,
    )
