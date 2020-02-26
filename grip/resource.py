from cornice.resource import add_view
from cornice.validators import marshmallow_validator
from urllib.parse import unquote

from pyramid.httpexceptions import HTTPNotFound
from sqlalchemy.orm.exc import NoResultFound

# Do not remove this line. Its is important for swagger
# from cornice_apispec import validators


class Meta(type):
    def __new__(mcs, name, bases, namespace):

        # collectin_get
        if "collection_get" not in namespace:

            def collection_get(self):
                return super(cls, self).collection_get()

        else:
            collection_get = namespace["collection_get"]

        if "collection_get_schema" in namespace and namespace["collection_get_schema"]:
            collection_get_schema = namespace["collection_get_schema"]
        else:
            collection_get_schema = None

        namespace["collection_get"] = add_view(
            collection_get,
            schema=collection_get_schema,
            validators=(marshmallow_validator,),
            content_type="application/vnd.api+json",
            # apispec_show=True,
            renderer="json_api",
            # permission="view",
        )

        # collection_post
        if "collection_post" not in namespace:

            def collection_post(self):
                return super(cls, self).collection_post()

        else:
            collection_post = namespace["collection_post"]

        if (
            "collection_post_schema" in namespace
            and namespace["collection_post_schema"]
        ):
            collection_post_schema = namespace["collection_post_schema"]
        else:
            collection_post_schema = None

        if (
            "collection_response_schemas" in namespace
            and namespace["collection_response_schemas"]
        ):
            collection_response_schemas = namespace["collection_response_schemas"]
        else:
            collection_response_schemas = None

        if hasattr(collection_post, 'grip_schema'):
            collection_post_schema = collection_post.grip_schema

        collection_post_validator = (marshmallow_validator,)

        if hasattr(collection_post, 'grip_validators'):
            collection_post_validator = (collection_post.grip_validators, )

        namespace["collection_post"] = add_view(
            collection_post,
            validators=collection_post_validator,
            # apispec_show=True,
            content_type="application/vnd.api+json",
            renderer="json_api",
            schema=collection_post_schema,
            apispec_response_schemas=collection_response_schemas,
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

        if "resource_get_schema" in namespace and namespace["resource_get_schema"]:
            resource_get_schema = namespace["resource_get_schema"]
        else:
            resource_get_schema = None

        if hasattr(get, 'grip_schema'):
            resource_get_schema = get.grip_schema

        resource_get_validators = (marshmallow_validator,)

        if hasattr(get, 'grip_validators'):
            import pytest; pytest.set_trace()
            resource_get_validators = (get.grip_validators,)

        namespace["get"] = add_view(
            get,
            # apispec_show=True,
            schema=resource_get_schema,
            validators=resource_get_validators,
            apispec_response_schemas=resource_response_schemas,
            renderer="json_api",
            content_type="application/vnd.api+json",
            # permission="view",
        )

        # post
        if "post" not in namespace:

            def post(self):
                return super(cls, self).post()

        else:
            post = namespace["post"]

        if "resource_post_schema" in namespace and namespace["resource_post_schema"]:
            resource_post_schema = namespace["resource_post_schema"]
        else:
            resource_post_schema = None

        namespace["post"] = add_view(
            post,
            validators=(marshmallow_validator,),
            # apispec_show=True,
            schema=resource_post_schema,
            # apispec_response_schemas=resource_response_schemas,
            renderer="json_api",
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


