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
from peewee import JOIN

from ..exceptions import BadRequest


class BaseHandler:

    __slots__ = ('model', '_order', 'q')

    def __init__(self, model):
        self.model = model
        self._order = self.model.id

    @staticmethod
    def parse_embeds(params):
        embeds = params.pop('_embeds', [])
        if embeds == '':
            return []
        if isinstance(embeds, str):
            return embeds.split(',')
        return embeds

    def join(self, table):
        property = getattr(self.model, table)
        model = property.rel_model
        if hasattr(property, 'field'):
            property = property.field
        return self.model.q.join_from(self.model, model, JOIN.LEFT_OUTER)

    def embeds(self, params):
        """
        Parses embeds and set joins on the query
        """
        embeds = self.parse_embeds(params)
        for embed in embeds:
            try:
                property = getattr(self.model, embed)
            except AttributeError:
                raise BadRequest('embedding_error', embed)
            model = property.rel_model
            if hasattr(property, 'field'):
                property = property.field
                model = self.model
            self.model.q.join(model, on=(property == model.id))
        return embeds
