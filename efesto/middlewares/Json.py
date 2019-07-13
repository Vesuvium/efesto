# -*- coding: utf-8 -*-
import rapidjson


class Json:

    def process_response(self, request, response, resource, success):
        if success:
            if type(response.body) == dict:
                response.body = rapidjson.dumps(response.body, datetime_mode=1,
                                                number_mode=7, uuid_mode=1)
