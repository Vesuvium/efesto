# -*- coding: utf-8 -*-
from efesto.exceptions import BadRequest
from efesto.middlewares import Msgpack

import msgpack
from msgpack.exceptions import ExtraData

from pytest import fixture, raises


@fixture
def pack():
    return Msgpack('config')


def test_msgpack_process_request(patch, http_request, pack):
    patch.object(msgpack, 'unpackb')
    pack.process_request(http_request, 'response')
    msgpack.unpackb.assert_called_with(http_request.bounded_stream.read(),
                                       raw=False)
    assert http_request.payload == msgpack.unpackb()


def test_msgpack_process_request__no_content(http_request, pack):
    http_request.content_length = 0
    assert pack.process_request(http_request, 'response') is None


def test_msgpack_process_request__bad_request(patch, http_request, pack):
    patch.object(msgpack, 'unpackb', side_effect=ExtraData('data', 'extra'))
    with raises(BadRequest):
        pack.process_request(http_request, 'response')


def test_msgpack_process_response(patch, response, pack):
    patch.object(msgpack, 'packb')
    response.body = {}
    pack.process_response('request', response, 'res', True)
    msgpack.packb.assert_called_with({})
    assert response.body == msgpack.packb()


def test_msgpack_process_response__fail(response, pack):
    result = pack.process_response('request', response, 'res', False)
    assert result is None


def test_msgpack_process_response__no_dict(response, pack):
    response.body = 'string'
    pack.process_response('request', response, 'res', True)
    response.set_header.assert_called_with('content-type',
                                           'application/msgpack')
