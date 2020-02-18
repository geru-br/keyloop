import marshmallow_jsonapi
from enum import Enum
import marshmallow
from marshmallow import fields
from marshmallow_enum import EnumField


from keyloop.interfaces.identity import IIdentity, IIdentitySource


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
        if contact_type_validation_map[data['type'].upper()](data['value']):
            data['valid_for_auth'] = True

        return data


class IdentitySchema(marshmallow_jsonapi.Schema):
    class Meta:
        type_ = "identity"

    id = fields.UUID(dump_only=True, attribute="uuid")

    username = fields.String(required=True)
    password = fields.String(required=True)
    name = fields.String(required=False)
    contacts = fields.List(fields.Nested(ContactSchema), required=False)

    # @marshmallow.validates_schema
    @marshmallow.post_load
    def validate_credentials(self, data, **kwargs):
        request = self.context["request"]
        registry = request.registry.settings["keyloop_adapters"]

        identity_provider = registry.lookup([IIdentity], IIdentitySource, request.context.realm)
        if not identity_provider:
            # need to find a way to return a 404 instead of a 400
            raise marshmallow.ValidationError("Realm failed")

        identity = identity_provider.get(data["username"])

        if not identity.login(data["username"], data["password"]):
            # need to find a way to return a 401 instead of a 400
            raise marshmallow.ValidationError("credentials failed")
