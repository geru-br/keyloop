
from pyramid.view import exception_view_config
from pyramid.exceptions import HTTPBadRequest


@exception_view_config(path_info='/api/v1/', context=Exception)
def HTTPErrorHandler(self):
    raise HTTPBadRequest ("")