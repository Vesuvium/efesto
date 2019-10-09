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
from efesto.exceptions import BadRequest, NotFound
from efesto.handlers import BaseHandler, Items

from falcon import HTTP_204

from peewee import DoesNotExist

from pytest import fixture, raises


@fixture
def item(magic):
    item = Items(magic())
    item.q = magic()
    return item


def test_item():
    assert issubclass(Items, BaseHandler)


def test_item_query(item):
    item.query({'id': 1})
    assert item.model.q == item.model.select().where()


def test_items_on_get(patch, magic, item, siren):
    patch.many(Items, ['query', 'embeds'])
    request = magic()
    response = magic()
    user = magic()
    params = {'user': user, 'id': 1}
    item.on_get(request, response, **params)
    Items.query.assert_called_with(params)
    Items.embeds.assert_called_with(request.params)
    user.do.assert_called_with('read', item.model.q, item.model)
    assert user.do().get.call_count == 1
    siren.__init__.assert_called_with(item.model, user.do().get(),
                                      request.path)
    siren.encode.assert_called_with(includes=Items.embeds())
    assert response.body == siren().encode()


def test_items_on_get__not_found(patch, magic, http_request, item):
    user = magic(do=magic(side_effect=DoesNotExist))
    with raises(NotFound):
        item.on_get(http_request, 'response', user=user, id=1)


def test_item_on_patch(magic, response, http_request, item, siren):
    user = magic()
    item.on_patch(http_request, response, user=user, id=1)
    item.model.select().where.assert_called_with(False)
    user.do.assert_called_with('edit', item.model.select().where(),
                               item.model)
    user.do().get().edit.assert_called_with(http_request.payload)
    siren.__init__.assert_called_with(item.model, user.do().get(),
                                      http_request.path)
    assert response.body == siren().encode()


def test_item_on_patch__badrequest(magic, http_request, item):
    user = magic()
    user.do().get().edit.return_value = None
    with raises(BadRequest):
        item.on_patch(http_request, 'response', user=user, id=1)


def test_items_on_patch__notfound(magic, http_request, item):
    user = magic(do=magic(side_effect=DoesNotExist))
    with raises(NotFound):
        item.on_patch(http_request, 'response', user=user, id=1)


def test_item_on_delete(patch, magic, item):
    request = magic()
    response = magic()
    user = magic()
    item.on_delete(request, response, user=user, id=1)
    item.model.delete().where.assert_called_with(False)
    user.do.assert_called_with('eliminate', item.model.delete().where(),
                               item.model)
    assert response.status == HTTP_204
