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
from efesto.exceptions import BadRequest
from efesto.middlewares import Json

from pytest import fixture, raises

import rapidjson


@fixture
def json():
    return Json('config', 'db')


def test_json_process_request(patch, http_request, json):
    patch.object(rapidjson, 'loads')
    json.process_request(http_request, 'response')
    rapidjson.loads.assert_called_with(http_request.bounded_stream.read())
    assert http_request.payload == rapidjson.loads()


def test_json_process_request__no_content(http_request, json):
    http_request.content_length = 0
    assert json.process_request(http_request, 'response') is None


def test_json_process_request__bad_payload(patch, http_request, json):
    patch.object(rapidjson, 'loads', side_effect=ValueError)
    with raises(BadRequest):
        json.process_request(http_request, 'response')


def test_json_process_response(patch, response, json):
    patch.object(rapidjson, 'dumps')
    response.body = {}
    json.process_response('request', response, 'res', True)
    rapidjson.dumps.assert_called_with({}, datetime_mode=1, number_mode=7,
                                       uuid_mode=1)
    assert response.body == rapidjson.dumps()


def test_json_process_response__string(response, json):
    response.body = 'body'
    json.process_response('request', response, 'res', True)
    assert response.body == 'body'


def test_json_process_response__fail(response, json):
    response.body = {}
    json.process_response('request', response, 'res', False)
    assert response.body == {}
