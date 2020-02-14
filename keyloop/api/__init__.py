from grip.renderers import json_api_renderer

def includeme(config):
    config.include(".v1", route_prefix="/v1")
    config.add_renderer('json_api', json_api_renderer)
