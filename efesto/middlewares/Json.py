# -*- coding: utf-8 -*-
import rapidjson

from ..exceptions import BadRequest


class Json:

    __slots__ = ()

    def __init__(self, config):
        pass

    def process_request(self, request, response):
        if request.content_length:
            try:
                payload = request.bounded_stream.read()
                request.payload = rapidjson.loads(payload)
            except ValueError:
                decoded_payload = payload.decode('utf-8')
                raise BadRequest('payload_error', decoded_payload, 'JSON')

    def process_response(self, request, response, resource, success):
        if success:
            if type(response.body) == dict:
                response.body = rapidjson.dumps(response.body, datetime_mode=1,
                                                number_mode=7, uuid_mode=1)
