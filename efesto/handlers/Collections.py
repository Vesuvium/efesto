# -*- coding: utf-8 -*
from falcon import HTTP_501

import rapidjson

from .BaseHandler import BaseHandler
from ..Siren import Siren


class Collections(BaseHandler):

    def query(self, params):
        self.model.q = self.model.select()
        for key, value in params.items():
            self.model.query(key, value)

    def page(self, params):
        self._page = int(params.pop('page', 1))

    def items(self, params):
        self._items = int(params.pop('items', 20))

    def order(self, params):
        """
        Sets _order to the requested order, or leaves it to the default value.
        """
        order = params.pop('_order', None)
        if order is None:
            return None
        column = getattr(self.model, order)
        if column is None:
            return None
        self._order = column

    @staticmethod
    def apply_owner(user, payload):
        if 'owner_id' in payload:
            return None
        payload['owner_id'] = user.id

    def process_params(self, params):
        """
        Processes the parameters of a request
        """
        self.page(params)
        self.items(params)
        self.order(params)
        self.query(params)

    def get_data(self, user):
        """
        Gets data performing a read query with the current user.
        """
        return user.do('read', self.model.q, self.model)

    def paginate_data(self, data):
        """
        Paginate data
        """
        query = data.order_by(self._order).paginate(self._page, self._items)
        return list(query.execute())

    def on_get(self, request, response, **params):
        """
        Executes a get request
        """
        user = params['user']
        self.process_params(request.params)
        embeds = self.embeds(request.params)
        data = self.get_data(user)
        body = Siren(self.model, self.paginate_data(data), request.path,
                     page=self._page, total=data.count())
        response.body = body.encode(includes=embeds)

    def on_post(self, request, response, **params):
        json = rapidjson.load(request.bounded_stream)
        self.apply_owner(params['user'], json)
        item = self.model.create(**json)
        body = Siren(self.model, item, request.path)
        response.body = body.encode()

    def on_patch(self, request, response, **params):
        response.status = HTTP_501
