# -*- coding: utf-8 -*-
from efesto.exceptions import BadRequest

from falcon import HTTPBadRequest


def test_bad_request():
    messsage = 'Cannot embed {} for this resource'
    assert BadRequest.errors['embedding_error'] == messsage
    assert BadRequest.errors['write_error'] == 'Cannot write {} to database'
    assert issubclass(BadRequest, HTTPBadRequest)


def test_bad_request_init():
    BadRequest.errors['error'] = 'message with {}'
    error = BadRequest('error', 'args')
    assert error.title == 'Bad request'
    assert error.description == 'message with args'
