# -*- coding: utf-8 -*-
from peewee import JOIN


class BaseHandler:
    def __init__(self, model):
        self.model = model
        self._order = self.model.id

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
        embeds = params.pop('_embeds', [])
        if isinstance(embeds, str):
            embeds = [embeds]
        for embed in embeds:
            self.model.q = self.join(embed)
        return embeds
