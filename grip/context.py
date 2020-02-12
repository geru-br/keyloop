from pyramid.security import Allow


class SimpleBaseFactory:
    def __init__(self, request):
        self.request = request