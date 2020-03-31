import marshmallow

from urllib.parse import unquote

from rqlalchemy.query import RQLQueryError


class RqlQueryStringSchema(marshmallow.Schema):
    @marshmallow.validates_schema(pass_many=True)
    def validate_unknown(self, data, **kwargs):

        request = self.context["request"]
        qs = unquote(request.query_string)

        try:
            query = request.context.model.query.rql(qs)
        except RQLQueryError as exc:
            raise marshmallow.ValidationError(str(exc))
