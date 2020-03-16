class Pagination:
    def __init__(self):
        self.first_page = None
        self.last_page = None
        self.prev_page = None
        self.next_page = None

    @staticmethod
    def _page_link_url(request, page_value):
        base_url = request.url.split('?')[0]
        query_args = {
            **request.params,
            'page[number]': page_value,
        }
        query_string = '&'.join([
            '{}={}'.format(k, v) for k, v in query_args.items()
        ])
        return '{}?{}'.format(base_url, query_string)

    def pagination_links(self, pagination_obj, request):
        self_ = request.url

        self.first_page = self._page_link_url(request, 1)
        self.last_page = self._page_link_url(request, pagination_obj.pages)

        if pagination_obj.has_previous:
            self.prev_page = self._page_link_url(request, pagination_obj.previous_page)

        if pagination_obj.has_next:
            self.next_page = self._page_link_url(request, pagination_obj.next_page)

        return {
            'self': self_,
            'first': self.first_page,
            'prev': self.prev_page,
            'next': self.next_page,
            'last': self.last_page
        }
