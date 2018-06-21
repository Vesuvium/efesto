# -*- coding: utf-8 -*-
from efesto.handlers import Items

from falcon import HTTPNotFound, HTTP_204

from peewee import DoesNotExist

from pytest import fixture, raises

import rapidjson


@fixture
def item(magic):
    return Items(magic())


def test_item_init():
    item = Items('model')
    assert item.model == 'model'


def test_items_on_get(patch, magic, item, siren):
    request = magic()
    response = magic()
    user = magic()
    item.on_get(request, response, user=user, id=1)
    item.model.select().where.assert_called_with(False)
    user.do.assert_called_with('read', item.model.select().where(),
                               item.model)
    assert user.do().get.call_count == 1
    siren.__init__.assert_called_with(item.model, user.do().get(),
                                      request.path)
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
