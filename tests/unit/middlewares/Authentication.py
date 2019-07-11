# -*- coding: utf-8 -*-
from efesto.middlewares import Authentication
from efesto.models import Users

from falcon import HTTPUnauthorized

import jwt
from jwt.exceptions import (DecodeError, ExpiredSignatureError,
                            InvalidAudienceError)

from pytest import fixture, mark, raises


@fixture
def auth():
    return Authentication('secret', 'audience', 'public')


def test_middleware_authentication_init(auth):
    assert auth.secret == 'secret'
    assert auth.audience == 'audience'
    assert auth.public_endpoints == ['public']


def test_middleware_unauthorized(auth):
    with raises(HTTPUnauthorized):
        auth.unauthorized()


def test_middleware_authentication_bearer_token(auth):
    """
    Ensures that a token can be fetched from the auth header
    """
    assert auth.bearer_token('Bearer token') == 'token'


@mark.parametrize('string', ['', 'bearer', 'token', 'no token'])
def test_authentication_bearer_token_none(patch, auth, string):
    """
    Ensures malformed tokens return None
    """
    patch.object(Authentication, 'unauthorized')
    assert auth.bearer_token(string) == Authentication.unauthorized()


def test_middleware_authentication_decode(patch, auth):
    patch.object(jwt, 'decode')
    result = auth.decode('token')
    jwt.decode.assert_called_with('token', auth.secret, audience=auth.audience)
    assert result == jwt.decode()


@mark.parametrize('error', [
    DecodeError, ExpiredSignatureError, InvalidAudienceError
])
def test_middleware_authentication_decode_error(patch, auth, error):
    patch.object(jwt, 'decode', side_effect=error)
    patch.object(Authentication, 'unauthorized')
    assert auth.decode('token') == Authentication.unauthorized()


def test_middleware_authentication_login(patch, auth):
    patch.object(Users, 'login')
    patch.many(Authentication, ['decode', 'bearer_token'])
    Authentication.decode.return_value = {'sub': 'sub'}
    result = auth.login('auth_header')
    Authentication.bearer_token.assert_called_with('auth_header')
    Authentication.decode.assert_called_with(Authentication.bearer_token())
    Users.login.assert_called_with('sub')
    assert result == Users.login()


@mark.parametrize('endpoint', ['/', '/endpoint', '/endpoint/id'])
def test_authentication_is_public(auth, endpoint):
    auth.public_endpoints = 'index,endpoint'
    assert auth.is_public(endpoint, 'get') is True


def test_authentication_is_public__method(auth):
    auth.public_endpoints = 'post:endpoint'
    assert auth.is_public('/endpoint', 'post') is True


@mark.parametrize('method', ['get', 'post', 'patch', 'delete'])
def test_authentication_is_public__all_methods(auth, method):
    auth.public_endpoints = '*:endpoint'
    assert auth.is_public('/endpoint', method) is True


def test_authentication_is_public__always(auth):
    auth.public_endpoints = '*'
    assert auth.is_public('/whatever', 'get') is True


def test_authentication_process_resource(patch, http_request, auth):
    patch.object(Authentication, 'login')
    result = auth.process_resource(http_request, 'res', 'resource', {})
    Authentication.login.assert_called_with(http_request.auth)
    assert result['user'] == Authentication.login()


def test_authentication_process_resource_no_auth(patch, http_request, auth):
    patch.object(Authentication, 'unauthorized')
    http_request.auth = None
    result = auth.process_resource(http_request, 'res', 'resource', {})
    assert result == Authentication.unauthorized()


def test_authentication_process_resource_no_user(patch, http_request, auth):
    patch.many(Authentication, ['login', 'unauthorized'])
    Authentication.login.return_value = None
    result = auth.process_resource(http_request, 'res', 'resource', {})
    assert result == auth.unauthorized()
