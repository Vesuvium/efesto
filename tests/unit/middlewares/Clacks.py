# -*- coding: utf-8 -*-
from efesto.middlewares import Clacks


def test_clacks_process_response(response):
    clacks = Clacks()
    clacks.process_response('request', response, 'resource', 'success')
    value = 'GNU Terry Pratchett'
    response.set_header.assert_called_with('X-Clacks-Overhead', value)
