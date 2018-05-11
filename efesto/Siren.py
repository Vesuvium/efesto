# -*- coding: utf-8 -*-
import ujson


class Siren:

    def __init__(self, model=None, data=[], path='', total=0, page=1):
        self.model = model
        self.data = data
        self.path = path
        self.total = total
        self.page = page

    def paginate(self, path, items, current_page, total_items):
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

    def make_entity(self, item):
        """
        Creates an entity from a model instance
        """
        href = '{}/{}'.format(self.path, item.id)
        if self.path.endswith('/{}'.format(item.id)):
            href = self.path
        return {
            'properties': item.__data__,
            'class': [item.__class__.__name__],
            'links': [
                {'href': href, 'rel': 'self'}
            ]
        }

    def make_entities(self):
        entities = []
        for item in self.data:
            entities.append(self.make_entity(item))

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

    def encode(self, *args):
        if type(self.data) == list:
            return ujson.dumps(self.make_entities())
        return ujson.dumps(self.make_entity(self.data))
