# -*- coding: utf-8 -*-
from efesto.handlers import BaseHandler

from pytest import fixture


@fixture
def handler(magic):
    handler = BaseHandler(magic())
    handler.q = magic()
    return handler


def test_basehandler_init(magic):
    model = magic()
    handler = BaseHandler(model)
    assert handler.model == model
    assert handler._order == model.id


def test_basehandler_parse_embeds():
    assert BaseHandler.parse_embeds({'_embeds': ['one']}) == ['one']


def test_basehandler_parse_embeds_string():
    assert BaseHandler.parse_embeds({'_embeds': 'one,two'}) == ['one', 'two']


def test_basehandler_parse_embeds_empty():
    assert BaseHandler.parse_embeds({}) == []


def test_basehandler_embeds(patch, handler, magic):
    patch.object(BaseHandler, 'parse_embeds', return_value=['one'])
    model = magic(one=magic(spec_set=['rel_model']))
    handler.model = model
    result = handler.embeds('params')
    BaseHandler.parse_embeds.assert_called_with('params')
    handler.model.q.join.assert_called_with(model.one.rel_model, on=False)
    assert result == BaseHandler.parse_embeds()


def test_basehandler_embeds_reverse(patch, handler):
    """
    Verifies that embeds work with backrefs.
    """
    patch.object(BaseHandler, 'parse_embeds', return_value=['one'])
    handler.embeds('params')
    handler.model.q.join.assert_called_with(handler.model, on=False)
