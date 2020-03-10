import marshmallow_jsonapi
from marshmallow import fields


class PermissionSchema(marshmallow_jsonapi.Schema):
    class Meta:
        type_ = "permission"

    id = fields.UUID(dump_only=True, attribute="uuid")
    name = fields.String(required=True)
    description = fields.String(required=True, validate=lambda x: True if x != "" else False)  # Empty string not acceptable


class PermissionGrantSchema(marshmallow_jsonapi.Schema):
    class Meta:
        type_ = "permission-grant"

    id = fields.UUID(dump_only=True, attribute="uuid")
    perm_name = fields.String(required=True)
