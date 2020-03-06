from enum import Enum

import marshmallow
import marshmallow_jsonapi
from marshmallow import fields
from marshmallow_enum import EnumField


class ContactType(Enum):
    EMAIL = "EMAIL"
    MSISDN = "MSISDN"
    PINTEREST_ID = "PINTEREST_ID"


def validate_msisdn(value):
    if str(value).isdigit() and len(value) == 11:
        return True

    return False


contact_type_validation_map = {
    ContactType.EMAIL.value: lambda x: True,
    ContactType.MSISDN.value: validate_msisdn,
    ContactType.PINTEREST_ID.value: lambda x: True,
}


class ContactSchema(marshmallow.Schema):
    type = EnumField(ContactType)  # ex. "email", "msisdn", "pinterest_id", etc
    value = fields.String()
    valid_for_auth = fields.Boolean(load_only=True)

    @marshmallow.pre_load
    def check_valid_contact_type_and_value(self, data, **kwargs):
        if contact_type_validation_map[data["type"].upper()](data["value"]):
            data["valid_for_auth"] = True

        return data

class BaseIdentitySchema(marshmallow_jsonapi.Schema):
    class Meta:
        type_ = "identity"

    id = fields.UUID(dump_only=True, attribute="id")
    name = fields.String(required=False)
    contacts = fields.List(fields.Nested(ContactSchema), required=False)
    permissions = fields.List(fields.String(), dump_only=True)


class IdentitySchema(BaseIdentitySchema):
    username = fields.String(required=True)
    password = fields.String(required=True)


class IdentityUpdateSchema(BaseIdentitySchema):
    username = fields.String(required=False)
    password = fields.String(required=False)
