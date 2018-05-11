# -*- coding: utf-8 -*-
from efesto.Siren import Siren
from efesto.handlers import Items

from falcon import HTTPNotFound, HTTP_204

from peewee import DoesNotExist

from pytest import fixture, raises


import ujson


@fixture
def item(magic):
    return Items(magic())


def test_item_init():
    item = Items('model')
    assert item.model == 'model'


def test_items_on_get(patch, magic, item):
    request = magic()
    response = magic()
    user = magic()
    patch.init(Siren)
    patch.object(Siren, 'encode')
    item.on_get(request, response, user=user, id=1)
    item.model.select().where.assert_called_with(False)
    user.do.assert_called_with('read', item.model.select().where(),
                               item.model)
    assert user.do().get.call_count == 1
    Siren.__init__.assert_called_with(item.model, user.do().get(),
                                      request.path)
    assert response.body == Siren().encode()


def test_items_on_get_404(patch, magic, item):
    request = magic()
    response = magic()
    user = magic(do=magic(side_effect=DoesNotExist))
    with raises(HTTPNotFound):
        item.on_get(request, response, user=user, id=1)


def test_item_on_patch(patch, magic, item):
    patch.init(Siren)
    patch.object(Siren, 'encode')
    patch.object(ujson, 'load')
    request = magic()
    response = magic()
    user = magic()
    item.on_patch(request, response, user=user, id=1)
    item.model.select().where.assert_called_with(False)
    user.do.assert_called_with('edit', item.model.select().where(),
                               item.model)
    assert user.do().get.call_count == 1
    Siren.__init__.assert_called_with(item.model, user.do().get(),
                                      request.path)
    assert response.body == Siren().encode()


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
