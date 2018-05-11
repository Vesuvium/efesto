# -*- coding: utf-8 -*-
import datetime

from efesto.Tokens import Tokens

import jwt
from jwt.exceptions import DecodeError, ExpiredSignatureError

from pytest import mark


def test_tokens_encode(patch):
    patch.object(jwt, 'encode')
    result = Tokens.encode('secret')
    jwt.encode.assert_called_with({}, 'secret')
    assert result == jwt.encode()


def test_tokens_encode_expiration(patch):
    patch.object(jwt, 'encode')
    patch.many(datetime, ['datetime', 'timedelta'])
    Tokens.encode('secret', expiration=100)
    assert datetime.datetime.utcnow.call_count == 1
    datetime.timedelta.assert_called_with(100)
    expiration = datetime.datetime.utcnow() + datetime.timedelta()
    jwt.encode.assert_called_with({'exp': expiration}, 'secret')


def test_tokens_encode_payload(patch):
    patch.object(jwt, 'encode')
    Tokens.encode('secret', sub='user')
    jwt.encode.assert_called_with({'sub': 'user'}, 'secret')


def test_middleware_authentication_decode(patch):
    patch.object(jwt, 'decode')
    result = Tokens.decode('secret', 'token')
    jwt.decode.assert_called_with('token', 'secret')
    assert result == jwt.decode()


@mark.parametrize('error', [DecodeError, ExpiredSignatureError])
def test_middleware_authentication_decode_error(patch, error):
    patch.object(jwt, 'decode', side_effect=error)
    assert Tokens.decode('secret', 'token') is None
