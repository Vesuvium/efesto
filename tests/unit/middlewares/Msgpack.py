# -*- coding: utf-8 -*-
from efesto.exceptions import BadRequest
from efesto.middlewares import Msgpack

import msgpack
from msgpack.exceptions import ExtraData

from pytest import raises


def test_msgpack_process_request(patch, http_request):
    patch.object(msgpack, 'unpackb')
    Msgpack().process_request(http_request, 'response')
    msgpack.unpackb.assert_called_with(http_request.bounded_stream.read(),
                                       raw=False)
    assert http_request.payload == msgpack.unpackb()


def test_msgpack_process_request__no_content(http_request):
    http_request.content_length = 0
    assert Msgpack().process_request(http_request, 'response') is None


def test_msgpack_process_request__bad_request(patch, http_request):
    patch.object(msgpack, 'unpackb', side_effect=ExtraData('data', 'extra'))
    with raises(BadRequest):
        Msgpack().process_request(http_request, 'response')


def test_msgpack_process_response(patch, response):
    patch.object(msgpack, 'packb')
    response.body = {}
    Msgpack().process_response('request', response, 'res', True)
    msgpack.packb.assert_called_with({})
    assert response.body == msgpack.packb()


def test_msgpack_process_response__fail(response):
    result = Msgpack().process_response('request', response, 'res', False)
    assert result is None


def test_msgpack_process_response__no_dict(response):
    response.body = 'string'
    Msgpack().process_response('request', response, 'res', True)
    response.set_header.assert_called_with('content-type',
                                           'application/msgpack')
