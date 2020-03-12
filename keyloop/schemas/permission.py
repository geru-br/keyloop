import marshmallow_jsonapi
import marshmallow
from marshmallow import fields


class PermissionSchema(marshmallow_jsonapi.Schema):
    class Meta:
        type_ = "permission"

    id = fields.UUID(dump_only=True, attribute="uuid")
    name = fields.String(required=True)
    description = fields.String(required=True, validate=lambda x: True if x != "" else False)  # Empty string not accepted


class PermissionQueryStringSchema(marshmallow.Schema):
    page = fields.Integer(validate=lambda x: True if x > 0 else False)  # Only number great than zero
    limit = fields.Integer(validate=lambda x: True if x > 0 else False)  # Only number great than zero


class PermissionGrantSchema(marshmallow_jsonapi.Schema):
    class Meta:
        type_ = "permission-grant"

    id = fields.UUID(dump_only=True, attribute="uuid")
    perm_name = fields.String(required=True)
