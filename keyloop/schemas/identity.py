import marshmallow_jsonapi
from marshmallow import fields


class BaseIdentitySchema(marshmallow_jsonapi.Schema):
    class Meta:
        type_ = "identity"

    id = fields.UUID(dump_only=True, attribute="id")
    name = fields.String(required=True)
    active = fields.Boolean()
    permissions = fields.List(fields.String(), dump_only=True)


class IdentitySchema(BaseIdentitySchema):
    username = fields.String(required=True)
    password = fields.String(required=True)


class IdentityUpdateSchema(BaseIdentitySchema):
    username = fields.String(required=False)
    password = fields.String(required=False)


class IdentityUpdatePasswordSchema(BaseIdentitySchema):
    last_password = fields.String(required=True)
    password = fields.String(required=True)
