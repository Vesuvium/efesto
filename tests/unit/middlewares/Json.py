# -*- coding: utf-8 -*-
from efesto.middlewares import Json

import rapidjson


def test_json_process_response(patch, response):
    patch.object(rapidjson, 'dumps')
    response.body = {}
    Json().process_response('request', response, 'res', True)
    rapidjson.dumps.assert_called_with({}, datetime_mode=1, number_mode=7,
                                       uuid_mode=1)
    assert response.body == rapidjson.dumps()


def test_json_process_response__string(response):
    response.body = 'body'
    Json().process_response('request', response, 'res', True)
    assert response.body == 'body'


def test_json_process_response__fail(response):
    response.body = {}
    Json().process_response('request', response, 'res', False)
    assert response.body == {}
