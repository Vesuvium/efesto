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
