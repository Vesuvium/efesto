# -*- coding: utf-8 -*-
from falcon import HTTP_204

from peewee import DoesNotExist

from .BaseHandler import BaseHandler
from ..Siren import Siren
from ..exceptions import BadRequest, NotFound


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
            raise NotFound()
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
            raise NotFound()
        if result.edit(request.payload) is None:
            raise BadRequest('write_error', request.payload)
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
