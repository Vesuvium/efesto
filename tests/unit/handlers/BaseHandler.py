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
from efesto.exceptions import BadRequest
from efesto.handlers import BaseHandler

from pytest import fixture, raises


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


def test_basehandler_parse_embeds__empty_string():
    assert BaseHandler.parse_embeds({'_embeds': ''}) == []


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


def test_basehandler_embeds__error(patch, handler, magic):
    patch.object(BaseHandler, 'parse_embeds', return_value=['one'])
    handler.model = 'model'
    with raises(BadRequest):
        handler.embeds('params')
