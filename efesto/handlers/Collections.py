# -*- coding: utf-8 -*
from falcon import HTTP_501

import ujson

from ..Siren import Siren


class Collections:
    def __init__(self, model):
        self.model = model

    def query(self, params):
        self.model.q = self.model.select()
        for key, value in params.items():
            self.model.query(key, value)
        return self.model.q

    def embeds(self, params):
        """
        Parses embeds and set joins on the query
        """
        embeds = params.pop('_embeds', None)
        if isinstance(embeds, str):
            embeds = [embeds]
        if embeds:
            for embed in embeds:
                model = getattr(self.model, embed).rel_model
                self.model.q.join(model, on=(self.model.second == model.id))
            return embeds
        return []

    @staticmethod
    def page(params):
        return int(params.pop('page', 1))

    @staticmethod
    def items(params):
        return int(params.pop('items', 20))

    def on_get(self, request, response, **params):
        """
        Executes a get request
        """
        user = params['user']
        page = self.page(request.params)
        items = self.items(request.params)
        query = self.query(request.params)
        embeds = self.embeds(request.params)
        result = user.do('read', query, self.model)
        paginated_query = result.paginate(page, items).execute()
        body = Siren(self.model, list(paginated_query), request.path,
                     page=page, total=result.count())
        response.body = body.encode(includes=embeds)

    def on_post(self, request, response, **params):
        json = ujson.load(request.bounded_stream)
        item = self.model.create(owner_id=params['user'].id, **json)
        body = Siren(self.model, item, request.path)
        response.body = body.encode()

    def on_patch(self, request, response, **params):
        response.status = HTTP_501
