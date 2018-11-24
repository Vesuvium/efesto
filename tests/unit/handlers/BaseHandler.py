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


def test_basehandler_embeds(handler, magic):
    model = magic(one=magic(spec_set=['rel_model']))
    handler.model = model
    result = handler.embeds({'_embeds': 'one'})
    handler.model.q.join.assert_called_with(model.one.rel_model, on=False)
    assert result == ['one']


def test_basehandler_embeds_reverse(handler):
    """
    Verifies that embeds work with backrefs.
    """
    result = handler.embeds({'_embeds': 'one'})
    model = handler.model
    model.one.field = 'field'
    handler.model.q.join.assert_called_with(model, on=False)
    assert result == ['one']


def test_basehandler_embeds_none(handler):
    result = handler.embeds({'_embeds': None})
    assert result == []
