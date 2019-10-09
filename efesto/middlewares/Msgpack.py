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
import msgpack
from msgpack.exceptions import ExtraData

from ..exceptions import BadRequest


class Msgpack:

    __slots__ = ()

    def __init__(self, config):
        pass

    def process_request(self, request, response):
        if request.content_length:
            try:
                payload = request.bounded_stream.read()
                request.payload = msgpack.unpackb(payload, raw=False)
            except ExtraData:
                raise BadRequest('payload_error', payload, 'MsgPack')

    def process_response(self, request, response, resource, success):
        if success:
            response.set_header('content-type', 'application/msgpack')
            if type(response.body) == dict:
                response.body = msgpack.packb(response.body)
