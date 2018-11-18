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


def test_basehandler_join(handler, magic):
    """
    Ensures join performs the joins correctly.
    """
    model = magic(one=magic(spec_set=['rel_model']))
    handler.model = model
    result = handler.join('one')
    handler.model.q.join.assert_called_with(model.one.rel_model, on=False)
    assert result == handler.model.q.join()


def test_basehandler_embeds(patch, handler, magic):
    """
    Ensures embeds updates the query and returns embeds.
    """
    patch.object(BaseHandler, 'join')
    result = handler.embeds({'_embeds': 'one'})
    BaseHandler.join.assert_called_with('one')
    assert handler.model.q == BaseHandler.join()
    assert result == ['one']


def test_basehandler_embeds_none(handler):
    result = handler.embeds({})
    assert result == []
