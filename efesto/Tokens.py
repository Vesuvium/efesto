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
import datetime

import jwt
from jwt.exceptions import DecodeError, ExpiredSignatureError


class Tokens:
    """
    Provides JWT encoding and decoding functionalities
    """

    __slots__ = ()

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
