# -*- coding: utf-8 -*
from falcon import HTTP_501

import rapidjson

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
                property = getattr(self.model, embed)
                model = property.rel_model
                if hasattr(property, 'field'):
                    property = property.field
                    model = self.model
                self.model.q.join(model, on=(property == model.id))
            return embeds
        return []

    @staticmethod
    def page(params):
        return int(params.pop('page', 1))

    @staticmethod
    def items(params):
        return int(params.pop('items', 20))

    @staticmethod
    def apply_owner(user, payload):
        if 'owner_id' in payload:
            return None
        payload['owner_id'] = user.id

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
        json = rapidjson.load(request.bounded_stream)
        self.apply_owner(params['user'], json)
        item = self.model.create(**json)
        body = Siren(self.model, item, request.path)
        response.body = body.encode()

    def on_patch(self, request, response, **params):
        response.status = HTTP_501
