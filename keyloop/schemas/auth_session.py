import marshmallow_jsonapi
import marshmallow

from keyloop.interfaces.identity import IIdentity, IIdentitySource


class AuthSessionSchema(marshmallow_jsonapi.Schema):
    class Meta:
        type_ = "auth-session"

    id = marshmallow.fields.UUID(dump_only=True, attribute="uuid")

    username = marshmallow.fields.String()
    password = marshmallow.fields.String()

    identity = marshmallow_jsonapi.fields.Relationship(
        type_="identity",
        self_url='/realms/{realm_slug}/identities/{identity_id}',
        self_url_kwargs={'realm_slug': 'REALM', "identity_id": "<identity.id>"},
        schema="IdentitySchema",
    )

    @marshmallow.post_load
    def validate_credentials(self, data, **kwargs):

        request = self.context["request"]
        registry = request.registry.settings["keyloop_adapters"]

        identity_provider = registry.lookup(
            [IIdentity], IIdentitySource, request.context.realm
        )
        if not identity_provider:
            # need to find a way to return a 404 instead of a 400
            raise marshmallow.ValidationError("Realm failed")

        identity = identity_provider.get(data["username"])

        if not identity.login(data["username"], data["password"]):
            # need to find a way to return a 401 instead of a 400
            raise marshmallow.ValidationError("credentials failed")

        # Fixme
        request.identity = identity
