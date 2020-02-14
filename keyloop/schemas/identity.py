import marshmallow_jsonapi
import marshmallow


class IdentitySchema(marshmallow_jsonapi.Schema):
    class Meta:
        type_ = "identity"

    id = marshmallow.fields.UUID(dump_only=True, attribute="uuid")
