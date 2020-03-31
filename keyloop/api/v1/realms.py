# from cornice import resource
#
# from marshmallow import Schema, fields
#
# from pyramid.security import Allow, Everyone
#
# from keyloop.models import Realm
#
#
# class RealmsFactory:
#     def __init__(self, request):
#         self.request = request
#
#     def __acl__(self):
#         if self.request.request_iface.getName().startswith("collection_"):
#             # It is a collection request
#             return [(Allow, Everyone, "view")]
#         # resource request
#         return [(Allow, Everyone, "view")]
#
#
# class RealmSchema(Schema):
#     name = fields.Str()
#     slug = fields.Str()
#     description = fields.Str(missing="")
#
#
# class RealmResource:
#     def __init__(self, request, context=None):
#         self.request = request
#         self.context = context
#
#     @resource.view(permission="view")
#     def collection_get(self):
#         realms = Realm.query.all()
#         return RealmSchema().dump(realms, many=True)
#
#     @resource.view(permission="view")
#     def get(self):
#         realm_slug = self.request.matchdict.get("realm_slug")
#         realm_model = Realm.query.filter_by(slug=realm_slug).first()
#         if not realm_model:
#             self.request.errors.add("body", "realm_slug", "Realm does not exist")
#             self.request.errors.status = 404
#             return
#         return RealmSchema().dump(realm_model)
#
#
# realm_resource = resource.add_resource(
#     RealmResource,
#     collection_path="/realms",
#     path="/realms/{realm_slug}",
#     factory=RealmsFactory,
#     cors_enabled=True,
#     cors_origins=["https://accounts.geru-local.com.br"],
#     cors_credentials=True,
# )
#
#
# def includeme(config):
#     config.add_cornice_resource(realm_resource)
