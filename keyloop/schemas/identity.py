import marshmallow_jsonapi
import marshmallow
from marshmallow import fields

from keyloop.interfaces.identity import IIdentity, IIdentitySource


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
    name = fields.String(required=False)
    contacts = fields.List(fields.Nested(ContactSchema), required=False)


    @marshmallow.validates_schema
    def validate_credentials(self, data, **kwargs):
        request = self.context["request"]
        registry = request.registry.settings["keyloop_adapters"]



        identity_provider = registry.lookup([IIdentity], IIdentitySource, request.context.realm)
        if not identity_provider:
            # realm not found
            # raise HTTPNotFound("No such realm")
            raise marshmallow.ValidationError("Realm failed")

        identity = identity_provider.get(data["username"])

        if not identity.login(data["username"], data["password"]):
            raise marshmallow.ValidationError("credentials failed")
