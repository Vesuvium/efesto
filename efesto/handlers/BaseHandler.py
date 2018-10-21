# -*- coding: utf-8 -*-


class BaseHandler:
    def __init__(self, model):
        self.model = model
        self._order = self.model.id

    def embeds(self, params):
        """
        Parses embeds and set joins on the query
        """
        embeds = params.pop('_embeds', None)
        if isinstance(embeds, str):
            embeds = [embeds]
        if embeds:
            for embed in embeds:
                property = getattr(self.model, embed)
                model = property.rel_model
                if hasattr(property, 'field'):
                    property = property.field
                    model = self.model
                self.model.q.join(model, on=(property == model.id))
            return embeds
        return []
