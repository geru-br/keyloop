from cornice.resource import add_view
from cornice.validators import marshmallow_validator
from urllib.parse import unquote

from pyramid.httpexceptions import HTTPNotFound
from sqlalchemy.orm.exc import NoResultFound


# Do not remove this line. Its is important for swagger
# from cornice_apispec import validators


def default_error_handler(request):
    import json

    response = request.response
    params = {'status': 'error', 'errors': request.errors}
    response.body = json.dumps(params).encode("utf-8")
    response.status_code = request.errors.status
    response.content_type = 'application/vnd.api+json'
    return response


def _unpack_decorated_args(func):
    schema = func.grip_schema if hasattr(func, 'grip_schema') else None
    response_schema = func.grip_response_schema if hasattr(func, 'grip_response_schema') else None
    validators = func.grip_validators if hasattr(func, 'grip_validators') else marshmallow_validator
    error_handler = func.grip_error_handler if hasattr(func, 'grip_error_handler') else default_error_handler
    factory = func.grip_factory if hasattr(func, 'grip_factory') else None
    return schema, response_schema, validators, error_handler, factory


class Meta(type):
    def __new__(mcs, name, bases, namespace):

        # collectin_get
        if "collection_get" not in namespace:

            def collection_get(self):
                return super(cls, self).collection_get()

        else:
            collection_get = namespace["collection_get"]

        collection_get_schema, \
        collection_get_response_schemas, \
        collection_get_validator, \
        collection_get_error_handler, \
        factory = _unpack_decorated_args(collection_get)

        namespace["collection_get"] = add_view(
            collection_get,
            schema=collection_get_schema,
            validators=(marshmallow_validator,),
            content_type="application/vnd.api+json",
            # apispec_show=True,
            renderer="json_api",
            factory=factory
            # permission="view",
        )

        # collection_post
        if "collection_post" not in namespace:

            def collection_post(self):
                return super(cls, self).collection_post()

        else:
            collection_post = namespace["collection_post"]

        collection_post_schema, \
        collection_post_response_schemas, \
        collection_post_validator, \
        collection_post_error_handler, \
        factory = _unpack_decorated_args(collection_post)

        namespace["collection_post"] = add_view(
            collection_post,
            validators=collection_post_validator,
            # apispec_show=True,
            content_type="application/vnd.api+json",
            renderer="json_api",
            schema=collection_post_schema,
            apispec_response_schemas=collection_post_response_schemas,
            error_handler=collection_post_error_handler,
            factory=factory
            # permission="edit",
        )

        if (
                "resource_response_schemas" in namespace
                and namespace["resource_response_schemas"]
        ):
            resource_response_schemas = namespace["resource_response_schemas"]
        else:
            resource_response_schemas = None

        # get
        if "get" not in namespace:

            def get(self):
                return super(cls, self).get()

        else:
            get = namespace["get"]

        resource_get_schema, \
        resource_get_response_schemas, \
        resource_get_validators, \
        resource_get_error_handler, \
        factory = _unpack_decorated_args(get)

        namespace["get"] = add_view(
            get,
            # apispec_show=True,
            schema=resource_get_schema,
            validators=resource_get_validators,
            apispec_response_schemas=resource_get_response_schemas,
            renderer="json_api",
            content_type="application/vnd.api+json",
            error_handler=resource_get_error_handler,
            factory=factory
            # permission="view",
        )

        # post
        if "post" not in namespace:

            def post(self):
                return super(cls, self).post()

        else:
            post = namespace["post"]

        resource_post_schema, \
        resource_post_response_schemas, \
        resource_post_validators, \
        resource_post_error_handler, \
        factory = _unpack_decorated_args(post)

        namespace["post"] = add_view(
            post,
            validators=(resource_post_validators,),
            # apispec_show=True,
            schema=resource_post_schema,
            apispec_response_schemas=resource_post_response_schemas,
            renderer="json_api",
            error_handler=resource_post_error_handler,
            factory=factory
            # permission="edit",
        )

        # delete
        if "delete" not in namespace:

            def delete(self):
                return super(cls, self).delete()

        else:
            delete = namespace["delete"]

        resource_delete_schema, \
        resource_delete_response_schemas, \
        resource_delete_validators, \
        resource_delete_error_handler, \
        factory = _unpack_decorated_args(delete)

        namespace["delete"] = add_view(
            delete,
            validators=(resource_delete_validators,),
            # apispec_show=True,
            schema=resource_delete_schema,
            apispec_response_schemas=resource_delete_response_schemas,
            renderer="json_api",
            error_handler=resource_delete_error_handler,
            factory=factory
            # permission="edit",
        )

        # put
        if "put" not in namespace:

            def put(self):
                return super(cls, self).put()

        else:
            put = namespace["put"]

        resource_put_schema, \
        resource_put_response_schemas, \
        resource_put_validators, \
        resource_put_error_handler, \
        factory_put = _unpack_decorated_args(put)

        namespace["put"] = add_view(
            put,
            validators=(resource_put_validators,),
            # apispec_show=True,
            schema=resource_put_schema,
            apispec_response_schemas=resource_put_response_schemas,
            renderer="json_api",
            error_handler=resource_put_error_handler,
            factory=factory_put
            # permission="edit",
        )

        cls = super(Meta, mcs).__new__(mcs, name, bases, namespace)
        return cls


class BaseResource(metaclass=Meta):
    collection_post_schema = None
    collection_response_schemas = None
    resource_post_schema = None
    resource_response_schemas = None

    def __init__(self, request, context=None):
        self.request = request
        self.context = context

    def collection_get(self):
        qs = unquote(self.request.query_string)
        return self.request.context.query.rql(qs)

    def get(self):
        try:
            return self.request.context.get()
        except NoResultFound:
            raise HTTPNotFound()
