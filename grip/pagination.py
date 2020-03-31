import json


class Pagination:
    def __init__(self, data={}, request=None, schema=None):
        self.data = data
        self.request = request
        self.schema = schema
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

    def _pagination_links(self):
        self_ = self.request.url

        self.first_page = self._page_link_url(self.request, 1)
        self.last_page = self._page_link_url(self.request, self.data.pages)

        if self.data.has_previous:
            self.prev_page = self._page_link_url(self.request, self.data.previous_page)

        if self.data.has_next:
            self.next_page = self._page_link_url(self.request, self.data.next_page)

        return {
            'self': self_,
            'first': self.first_page,
            'prev': self.prev_page,
            'next': self.next_page,
            'last': self.last_page
        }

    def dumps(self):
        params = {
            "data": json.loads(self.schema.dumps(self.data.items).data)['data'],
            "links": self._pagination_links(),
            "meta": {
                "count": self.data.total,
                "total_pages": self.data.pages
            }
        }

        return json.dumps(params)
