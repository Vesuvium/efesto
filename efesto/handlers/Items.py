# -*- coding: utf-8 -*-
from falcon import HTTPNotFound, HTTP_204

from peewee import DoesNotExist

import rapidjson

from .BaseHandler import BaseHandler
from ..Siren import Siren


class Items(BaseHandler):

    def query(self, params):
        self.model.q = self.model.select().where(self.model.id == params['id'])

    def on_get(self, request, response, **params):
        """
        Executes a get request on a single item
        """
        user = params['user']
        self.query(params)
        embeds = self.embeds(request.params)
        try:
            result = user.do('read', self.model.q, self.model).get()
        except DoesNotExist:
            raise HTTPNotFound()
        body = Siren(self.model, result, request.path)
        response.body = body.encode(includes=embeds)

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
        json = rapidjson.load(request.bounded_stream)
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
