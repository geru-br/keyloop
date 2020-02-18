import marshmallow_jsonapi
import marshmallow

from .identity import IdentitySchema



class AuthSessionSchema(marshmallow_jsonapi.Schema):
    class Meta:
        type_ = "auth-session"

    id = marshmallow.fields.UUID(dump_only=True, attribute="uuid")

    identity = marshmallow.fields.Nested(IdentitySchema)
