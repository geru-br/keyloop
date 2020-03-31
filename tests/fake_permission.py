import math

from keyloop.api.v1.exceptions import PermissionAlreadyExists, PermissionNotFound
from keyloop.utils import generate_uuid


class Page(object):
    def __init__(self, items, page, page_size, total):
        self.items = items
        self.previous_page = None
        self.next_page = None
        self.has_previous = page > 1
        if self.has_previous:
            self.previous_page = page - 1
        previous_items = (page - 1) * page_size
        self.has_next = previous_items + len(items) < total
        if self.has_next:
            self.next_page = page + 1
        self.total = total
        self.pages = int(math.ceil(total / float(page_size)))


class FakePermission:
    PERMISSIONS = {}

    def __init__(self, name, description, uuid=None, document_meta=None):
        self.uuid = uuid if uuid else generate_uuid()
        self.name = name
        self.description = description
        self.document_meta = document_meta

    @classmethod
    def test_reset(cls):
        cls.PERMISSIONS = {}

    @classmethod
    def _get_by_name(cls, name):
        for perm in cls.PERMISSIONS.values():
            if perm['name'] == name:
                return cls(**perm)

        raise PermissionNotFound()

    @classmethod
    def get(cls, uuid=None, name=None):
        if name:
            return cls._get_by_name(name)
        elif uuid:
            params = cls.PERMISSIONS.get(uuid)
            if not params:
                raise PermissionNotFound()
            return cls(**params)

    @classmethod
    def create(cls, name, description):
        try:
            cls.get(name=name)
        except PermissionNotFound:
            permission = cls(name, description)
            cls.PERMISSIONS.update({permission.uuid: permission.__dict__})
            return permission
        else:
            raise PermissionAlreadyExists

    @classmethod
    def list(cls, page, limit):
        params = []
        total = len(cls.PERMISSIONS) if limit > len(cls.PERMISSIONS) else limit
        current_page = 0 if page in (0, 1) else page

        if not cls.PERMISSIONS:
            return Page([], current_page, limit, total)

        params.append(list(cls.PERMISSIONS.items())[0][1])
        return Page(params[current_page:total], current_page, limit, total)
