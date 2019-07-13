# -*- coding: utf-8 -*-
from peewee import JOIN

from ..exceptions import BadRequest


class BaseHandler:
    def __init__(self, model):
        self.model = model
        self._order = self.model.id

    @staticmethod
    def parse_embeds(params):
        embeds = params.pop('_embeds', [])
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
