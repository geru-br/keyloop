import marshmallow


class BasePathSchema(marshmallow.Schema):
    id = marshmallow.fields.UUID(required=True, dump_only=True)

    realm_slug = marshmallow.fields.String()
