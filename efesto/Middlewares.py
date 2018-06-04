# -*- coding: utf-8 -*-
from efesto.models import Users

from falcon import HTTPUnauthorized

import jwt
from jwt.exceptions import DecodeError, ExpiredSignatureError


class Authentication:

    def __init__(self, secret, audience):
        self.secret = secret
        self.audience = audience

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
        except (DecodeError, ExpiredSignatureError):
            return self.unauthorized()

    def login(self, payload):
        if 'sub' in payload:
            return Users.login(payload['sub'])
        return self.unauthorized()

    def process_resource(self, request, response, resource, params):
        if request.auth is None:
            return self.unauthorized()

        token = self.bearer_token(request.auth)
        payload = self.decode(token)
        user = self.login(payload)
        if user is None:
            return self.unauthorized()
        params['user'] = user
