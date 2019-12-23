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


class BaseHandler:

    __slots__ = ('model', '_order', 'q')

    def __init__(self, model):
        self.model = model
        self._order = 'id'

    @staticmethod
    def parse_embeds(params):
        embeds = params.pop('_embeds', [])
        if embeds == '':
            return []
        if isinstance(embeds, str):
            return embeds.split(',')
        return embeds

    def embeds(self, params):
        """
        Parses embeds and set joins on the query
        """
        embeds = self.parse_embeds(params)
        for embed in embeds:
            self.model.q.join(embed, self.model.foreign_column_for(embed))
        return embeds
