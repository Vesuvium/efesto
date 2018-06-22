# -*- coding: utf-8 -*-
from peewee import ModelSelect

import rapidjson


class Siren:

    def __init__(self, model=None, data=[], path='', total=0, page=1):
        self.model = model
        self.data = data
        self.path = path
        self.total = total
        self.page = page

    @staticmethod
    def paginate(path, items, current_page, total_items):
        links = [
            {'rel': ['self'], 'href': path}
        ]

        if total_items > len(items)*current_page:
            href = '{}?page={}'.format(path, current_page + 1)
            links.append({'rel': ['next'], 'href': href})

        if current_page != 1:
            href = '{}?page={}'.format(path, current_page - 1)
            links.append({'rel': ['previous'], 'href': href})
        return links

    @classmethod
    def nested_entities(cls, include, item):
        """
        Parses nested entities. Used when a join is performed and thus
        there are nested item to encode.
        """
        nested = getattr(item, include)
        if isinstance(nested, ModelSelect):
            nested = list(nested)
            items = []
            if len(nested) > 0:
                path = '/{}'.format(nested[0].__class__.__name__)
            for item in nested:
                items.append(cls.entity(path, item))
            return items
        path = '/{}'.format(nested.__class__.__name__)
        return cls.entity(path, nested)

    @classmethod
    def entity(cls, path, item, includes=[]):
        """
        Creates an entity from a model instance
        """
        href = '{}/{}'.format(path, item.id)
        if path.endswith('/{}'.format(item.id)):
            href = path

        for include in includes:
            item.__data__[include] = cls.nested_entities(include, item)

        return {
            'properties': item.__data__,
            'class': [item.__class__.__name__],
            'links': [
                {'href': href, 'rel': 'self'}
            ]
        }

    def entities(self, includes=[]):
        entities = []
        for item in self.data:
            entities.append(self.entity(self.path, item, includes=includes))

        fields = []
        name = 'add-item'
        if self.model:
            fields = self.model.get_columns()
            name = 'add-' + self.model._meta.name

        actions = [
            {'name': name, 'method': 'POST', 'type': 'application/json',
             'fields': fields}
        ]
        links = self.paginate(self.path, self.data, self.page, self.total)
        return {'entities': entities, 'actions': actions, 'links': links}

    def encode(self, *args, includes=[]):
        if isinstance(self.data, list):
            return rapidjson.dumps(self.entities(includes=includes),
                                   datetime_mode=1)
        output = self.entity(self.path, self.data, includes=includes)
        return rapidjson.dumps(output, datetime_mode=1)
