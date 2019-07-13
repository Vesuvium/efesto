# -*- coding: utf-8 -*-
from efesto.exceptions import NotFound

from falcon import HTTPNotFound


def test_not_found():
    assert issubclass(NotFound, HTTPNotFound)


def test_not_found_init():
    error = NotFound()
    assert error.title == 'Not found'
    assert error.description == 'The requested resource was not found'
