#   Copyright (C) 2018  Jacopo Cascioli
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
# -*- coding: utf-8 -*-


class Siren:

    __slots__ = ()

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
    def entity(cls, item, item_type, path, includes=[]):
        """
        Creates an entity from a model instance
        """
        href = f'{path}/{item["id"]}'
        if path.endswith(f'/{item["id"]}'):
            href = path

        for include in includes:
            item[include] = [
                cls.entity(n, include, f'/{include}') for n in item[include]
            ]

        return {
            'properties': item,
            'class': [item_type.lower()],
            'links': [
                {'href': href, 'rel': 'self'}
            ]
        }

    @classmethod
    def field_type(cls, value):
        try:
            int(value)
            return 'number'
        except ValueError:
            return 'text'

    @classmethod
    def fields(cls, data):
        return [{key: cls.field_type(value)} for key, value in data[0].items()]

    @classmethod
    def entities(cls, data, item_type, path, includes, page, total):
        entities = [
            cls.entity(item, item_type, path, includes) for item in data
        ]

        fields = cls.fields(data)
        name = f'add-{item_type}'

        actions = [
            {'name': name, 'method': 'POST', 'type': 'application/json',
             'fields': fields}
        ]
        links = cls.paginate(path, data, page, total)
        return {'entities': entities, 'actions': actions, 'links': links}

    @classmethod
    def encode(cls, data, includes, item_type, path, page, total):
        if type(data) == list:
            return cls.entities(data, item_type, path, includes, page, total)
        return cls.entity(data, item_type, path, includes)
