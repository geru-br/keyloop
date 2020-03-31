from .renderers import json_api_renderer

def includeme(config):
    config.add_renderer('json_api', json_api_renderer)
    config.add_renderer(None, json_api_renderer)