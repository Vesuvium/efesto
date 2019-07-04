# -*- coding: utf-8 -*-
from efesto.middlewares import Authentication
from efesto.models import Users

from falcon import HTTPUnauthorized

import jwt
from jwt.exceptions import (DecodeError, ExpiredSignatureError,
                            InvalidAudienceError)

from pytest import fixture, mark, raises


@fixture
def authentication():
    return Authentication('secret', 'audience')


def test_middleware_authentication_init(authentication):
    assert authentication.secret == 'secret'
    assert authentication.audience == 'audience'


def test_middleware_unauthorized(authentication):
    with raises(HTTPUnauthorized):
        authentication.unauthorized()


def test_middleware_authentication_bearer_token(authentication):
    """
    Ensures that a token can be fetched from the auth header
    """
    assert authentication.bearer_token('Bearer token') == 'token'


@mark.parametrize('string', ['', 'bearer', 'token', 'no token'])
def test_authentication_bearer_token_none(patch, authentication, string):
    """
    Ensures malformed tokens return None
    """
    patch.object(Authentication, 'unauthorized')
    assert authentication.bearer_token(string) == Authentication.unauthorized()


def test_middleware_authentication_decode(patch, authentication):
    patch.object(jwt, 'decode')
    result = authentication.decode('token')
    jwt.decode.assert_called_with('token', authentication.secret,
                                  audience=authentication.audience)
    assert result == jwt.decode()


@mark.parametrize('error', [
    DecodeError, ExpiredSignatureError, InvalidAudienceError
])
def test_middleware_authentication_decode_error(patch, authentication, error):
    patch.object(jwt, 'decode', side_effect=error)
    patch.object(Authentication, 'unauthorized')
    assert authentication.decode('token') is Authentication.unauthorized()


def test_middleware_authentication_login(patch, authentication):
    patch.object(Users, 'login')
    result = authentication.login({'sub': 'identifier'})
    Users.login.assert_called_with('identifier')
    assert result == Users.login()


def test_middleware_authentication_login_bad_payload(patch, authentication):
    patch.object(Users, 'login', return_value=None)
    patch.object(Authentication, 'unauthorized')
    assert authentication.login({}) == Authentication.unauthorized()


def test_authentication_process_resource(patch, magic, authentication):
    request = magic()
    params = {}
    patch.many(Authentication, ['bearer_token', 'decode', 'login'])
    authentication.process_resource(request, magic(), magic(), params)
    Authentication.bearer_token.assert_called_with(request.auth)
    Authentication.decode.assert_called_with(Authentication.bearer_token())
    Authentication.login.assert_called_with(Authentication.decode())
    assert params['user'] == authentication.login()


def test_authentication_process_resource_no_auth(patch, magic, authentication):
    request = magic(auth=None)
    patch.object(Authentication, 'unauthorized')
    result = authentication.process_resource(request, magic(), magic(), {})
    assert result == Authentication.unauthorized()


def test_authentication_process_resource_no_user(patch, magic, authentication):
    patch.many(Authentication, ['bearer_token', 'decode', 'login',
                                'unauthorized'])
    Authentication.login.return_value = None
    result = authentication.process_resource(magic(), magic(), magic(), {})
    assert result == authentication.unauthorized()
