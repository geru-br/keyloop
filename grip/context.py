class SimpleBaseFactory:

    def __init__(self, request):
        self.request = request

    @property
    def realm(self):
        return self.request.matchdict["realm_slug"]

    @property
    def validated(self):
        return self.request.validated["body"]
