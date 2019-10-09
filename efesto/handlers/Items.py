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
