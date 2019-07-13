# -*- coding: utf-8 -*-
from falcon import HTTPBadRequest


class BadRequest(HTTPBadRequest):

    errors = {
        'embedding_error': 'Cannot embed {} for this resource'
    }

    def __init__(self, error_type, *args):
        super().__init__('Bad request', self.errors[error_type].format(*args))
