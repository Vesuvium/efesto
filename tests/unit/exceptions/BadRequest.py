# -*- coding: utf-8 -*-
from efesto.exceptions import BadRequest

from falcon import HTTPBadRequest


def test_bad_request():
    messsage = 'Cannot embed {} for this resource'
    assert BadRequest.errors['embedding_error'] == messsage
    assert issubclass(BadRequest, HTTPBadRequest)


def test_bad_request_init():
    error = BadRequest('embedding_error', 'embed')
    assert error.title == 'Bad request'
    assert error.description == 'Cannot embed embed for this resource'
