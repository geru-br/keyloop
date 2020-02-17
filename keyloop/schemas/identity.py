import marshmallow_jsonapi
import marshmallow
from marshmallow import fields


class ContactSchema(marshmallow.Schema):
    type = fields.String() #  ex. "email", "msisdn", "pinterest_id", etc
    value = fields.String()
    valid_for_auth = fields.Boolean(default=True)


class IdentitySchema(marshmallow_jsonapi.Schema):
    class Meta:
        type_ = "identity"

    id = fields.UUID(dump_only=True, attribute="uuid")

    username = fields.String()
    password = fields.String()
    name = fields.String()
    contacts = fields.Nested(fields.List[ContactSchema])


