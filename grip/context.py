class SimpleBaseFactory:

    def __init__(self, request):
        self.request = request

    @property
    def realm(self):
        return self.request.validated["path"]["realm_slug"]

    @property
    def validated(self):
        return self.request.validated["body"]
