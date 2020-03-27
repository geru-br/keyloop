import marshmallow
import marshmallow_jsonapi
from marshmallow import fields, validate


class BaseSchema(marshmallow_jsonapi.Schema):
    class Meta:
        type_ = "permission"

    id = fields.UUID(dump_only=True, attribute="uuid")


class PermissionSchema(BaseSchema):
    # TODO: Add information about context.
    name = fields.String(required=True, validate=validate.Length(min=1))
    description = fields.String(required=True, validate=validate.Length(min=1))


class PermissionQueryStringSchema(marshmallow.Schema):
    page = fields.Integer(validate=lambda x: True if x > 0 else False,
                          load_from="page[number]")  # Only number great than zero
    limit = fields.Integer(validate=lambda x: True if x > 0 else False,
                           load_from="page[size]")  # Only number great than zero


class PermissionGrantSchema(marshmallow_jsonapi.Schema):
    class Meta:
        type_ = "permission-grant"

    id = fields.UUID(dump_only=True, attribute="uuid")
    perm_name = fields.String(required=True)
