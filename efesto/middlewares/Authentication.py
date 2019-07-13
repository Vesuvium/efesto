# -*- coding: utf-8 -*-
from falcon import HTTPUnauthorized

import jwt
from jwt.exceptions import (DecodeError, ExpiredSignatureError,
                            InvalidAudienceError)

from ..models import Users


class Authentication:

    def __init__(self, secret, audience, public_endpoints):
        self.secret = secret
        self.audience = audience
        self.public_endpoints = public_endpoints.split(',')

    @staticmethod
    def unauthorized():
        """
        Raises a 401 error
        """
        raise HTTPUnauthorized('Login required', 'Please login',
                               ['Bearer realm="login required"'])

    def bearer_token(self, auth_header):
        """
        Get the token from the auth header
        """
        shards = auth_header.split()
        if len(shards) == 2:
            if shards[0] == 'Bearer':
                return shards[1]
        return self.unauthorized()

    def decode(self, token):
        """
        Decode a token
        """
        try:
            return jwt.decode(token, self.secret, audience=self.audience)
        except (DecodeError, ExpiredSignatureError, InvalidAudienceError):
            return self.unauthorized()

    def login(self, authentication):
        payload = self.decode(self.bearer_token(authentication))
        if 'sub' in payload:
            return Users.login(payload['sub'])

    def is_public(self, path, method):
        """
        Whether a path and method are public endpoints. Public endpoints can
        be defined as a comma-separated list of values. Examples:
        'index,version', 'get:users', '*:users'
        """
        endpoint = path.split('/')[1]
        if self.public_endpoints == '*':
            return True
        elif endpoint == '':
            if 'index' in self.public_endpoints:
                return True
        elif endpoint in self.public_endpoints:
            return True
        elif f'{method}:{endpoint}' in self.public_endpoints:
            return True
        elif f'*:{endpoint}' in self.public_endpoints:
            return True

    def process_resource(self, request, response, resource, params):
        if self.is_public(request.path, request.method):
            return None
        if request.auth:
            user = self.login(request.auth)
            if user:
                params['user'] = user
                return params
        return self.unauthorized()
