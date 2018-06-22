# -*- coding: utf-8 -*-
from efesto.handlers import BaseHandler, Items

from falcon import HTTPNotFound, HTTP_204

from peewee import DoesNotExist

from pytest import fixture, raises

import rapidjson


@fixture
def item(magic):
    item = Items(magic())
    item.q = magic()
    return item


def test_item():
    assert issubclass(Items, BaseHandler)


def test_item_query(item):
    item.query({'id': 1})
    assert item.q == item.model.select().where()


def test_items_on_get(patch, magic, item, siren):
    patch.many(Items, ['query', 'embeds'])
    request = magic()
    response = magic()
    user = magic()
    params = {'user': user, 'id': 1}
    item.on_get(request, response, **params)
    Items.query.assert_called_with(params)
    Items.embeds.assert_called_with(params)
    user.do.assert_called_with('read', item.q, item.model)
    assert user.do().get.call_count == 1
    siren.__init__.assert_called_with(item.model, user.do().get(),
                                      request.path)
    siren.encode.assert_called_with(includes=Items.embeds())
    assert response.body == siren().encode()


def test_items_on_get_404(patch, magic, item):
    request = magic()
    response = magic()
    user = magic(do=magic(side_effect=DoesNotExist))
    with raises(HTTPNotFound):
        item.on_get(request, response, user=user, id=1)


def test_item_on_patch(patch, magic, item, siren):
    patch.object(rapidjson, 'load')
    request = magic()
    response = magic()
    user = magic()
    item.on_patch(request, response, user=user, id=1)
    item.model.select().where.assert_called_with(False)
    user.do.assert_called_with('edit', item.model.select().where(),
                               item.model)
    assert user.do().get.call_count == 1
    siren.__init__.assert_called_with(item.model, user.do().get(),
                                      request.path)
    assert response.body == siren().encode()


def test_items_on_patch_404(patch, magic, item):
    request = magic()
    response = magic()
    user = magic(do=magic(side_effect=DoesNotExist))
    with raises(HTTPNotFound):
        item.on_patch(request, response, user=user, id=1)


def test_item_on_delete(patch, magic, item):
    request = magic()
    response = magic()
    user = magic()
    item.on_delete(request, response, user=user, id=1)
    item.model.delete().where.assert_called_with(False)
    user.do.assert_called_with('eliminate', item.model.delete().where(),
                               item.model)
    assert response.status == HTTP_204
