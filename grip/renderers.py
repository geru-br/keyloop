import datetime
import enum
import uuid
from ipaddress import _IPAddressBase
import marshmallow

from pyramid.renderers import JSON
from sqlalchemy.ext.associationproxy import _AssociationList


class JsonApi(JSON):
    def _get_schema(self, system):

        schema = system["view"].__views__[0]["apispec_response_schemas"][200]
        return schema

    def __call__(self, info):
        def _render(value, system):
            schema = self._get_schema(system)

            # If schema is not an instance lets initialize it
            if not isinstance(schema, marshmallow.Schema):
                schema = schema()

            request = system.get("request")
            if request is not None:
                response = request.response
                response.content_type = "application/vnd.api+json"
                schema.context = {"request": request}

            return schema.dumps(value).data

        return _render


json_api_renderer = JsonApi()

json_api_renderer.add_adapter(datetime.datetime, lambda x, req: x.isoformat())
json_api_renderer.add_adapter(datetime.date, lambda x, req: x.isoformat())
json_api_renderer.add_adapter(uuid.UUID, lambda x, req: x.hex)
json_api_renderer.add_adapter(enum.Enum, lambda x, req: x.name)
json_api_renderer.add_adapter(_AssociationList, lambda x, req: list(x[:]))
json_api_renderer.add_adapter(_IPAddressBase, lambda x, req: str(x))
