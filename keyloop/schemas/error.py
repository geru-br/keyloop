import marshmallow_jsonapi
from marshmallow import fields


class ErrorSchema(marshmallow_jsonapi.Schema):
    class Meta:
        type_ = "error"

    id = fields.Int(dump_only=True)
    message = fields.String(dump_only=True)
