# -*- coding: utf-8 -*-
from falcon import HTTPNotFound, HTTP_204

from peewee import DoesNotExist

import ujson

from ..Siren import Siren


class Items:
    def __init__(self, model):
        self.model = model

    def on_get(self, request, response, **params):
        """
        Executes a get request on a single item
        """
        user = params['user']
        query = self.model.select().where(self.model.id == params['id'])
        try:
            result = user.do('read', query, self.model).get()
        except DoesNotExist:
            raise HTTPNotFound()
        body = Siren(self.model, result, request.path)
        response.body = body.encode()

    def on_patch(self, request, response, **params):
        """
        Executes a patch request on a single item
        """
        user = params['user']
        query = self.model.select().where(self.model.id == params['id'])
        try:
            result = user.do('edit', query, self.model).get()
        except DoesNotExist:
            raise HTTPNotFound()
        json = ujson.load(request.bounded_stream)
        result.update_item(json)
        body = Siren(self.model, result, request.path)
        response.body = body.encode()

    def on_delete(self, request, response, **params):
        """
        Executes a delete request on a single item
        """
        user = params['user']
        query = self.model.delete().where(self.model.id == params['id'])
        user.do('eliminate', query, self.model).execute()
        response.status = HTTP_204
