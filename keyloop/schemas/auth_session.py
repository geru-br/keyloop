import arrow
import marshmallow_jsonapi
import marshmallow

from keyloop.interfaces.identity import IIdentity, IIdentitySource
from keyloop.interfaces.auth_session import IAuthSession, IAuthSessionSource


class AuthSessionSchema(marshmallow_jsonapi.Schema):
    class Meta:
        type_ = "auth-session"

    id = marshmallow.fields.UUID(dump_only=True, attribute="uuid")

    active = marshmallow.fields.Bool(dump_only=True)
    start = marshmallow.fields.DateTime(dump_only=True)
    ttl = marshmallow.fields.Integer(dump_only=True)

    identity = marshmallow_jsonapi.fields.Relationship(
        type_="identity",
        self_url='/realms/{realm_slug}/identities/{identity_id}',
        self_url_kwargs={'realm_slug': 'REALM', "identity_id": "<identity.id>"},
        schema="IdentitySchema",
        dump_only=True,
    )

    @marshmallow.pre_load
    def load_identity(self, data, **kwargs):
        # import pdb
        # pdb.set_trace()
        # new_data = self.format_json_api_response(data, False)
        data['bla'] = "bla"
        return data

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

        import pdb
        pdb.set_trace()
        identity = identity_provider.get(data["username"])

        if not identity.login(data["username"], data["password"]):
            # need to find a way to return a 401 instead of a 400
            raise marshmallow.ValidationError("credentials failed")

        session_provider = registry.lookup(
            [IAuthSession], IAuthSessionSource, request.context.realm
        )
        auth_session = session_provider.create(identity=identity,
                                               ttl=600,
                                               active=True,
                                               start=arrow.utcnow().datetime)

        # Fixme
        request.identity = identity
        request.auth_session = auth_session
