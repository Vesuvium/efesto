# -*- coding: utf-8 -*-
import datetime

import jwt
from jwt.exceptions import DecodeError, ExpiredSignatureError


class Tokens:
    """
    Provides JWT encoding and decoding functionalities
    """

    @staticmethod
    def encode(secret, expiration=0, **kwargs):
        payload = {**kwargs}
        if expiration:
            now = datetime.datetime.utcnow()
            payload['exp'] = now + datetime.timedelta(expiration)
        return jwt.encode(payload, secret)

    @staticmethod
    def decode(secret, token):
        try:
            return jwt.decode(token, secret)
        except (DecodeError, ExpiredSignatureError):
            return None
