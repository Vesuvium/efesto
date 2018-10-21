# -*- coding: utf-8 -*-
from efesto.handlers import BaseHandler, Collections

from falcon import HTTP_501

from pytest import fixture

import rapidjson


@fixture
def collection(magic):
    collection = Collections(magic())
    collection.q = magic()
    return collection


def test_collection():
    assert issubclass(Collections, BaseHandler)


def test_collection_query(collection):
    collection.query({})
    assert collection.model.q == collection.model.select()


def test_collection_query_params(collection):
    collection.query({'key': 'value'})
    collection.model.query.assert_called_with('key', 'value')


def test_collection_page(collection):
    collection.page({'page': '2'})
    assert collection._page == 2


def test_collection_page_none(collection):
    collection.page({})
    assert collection._page == 1


def test_collection_items(collection):
    collection.items({'items': '2'})
    assert collection._items == 2


def test_collection_items_none(collection):
    collection.items({})
    assert collection._items == 20


def test_collection_order(collection):
    """
    Ensures Collections.order can extract the _order parameter
    """
    collection.order({'_order': 'rank'})
    assert collection._order == collection.model.rank


def test_collection_order_no_column(collection):
    """
    Ensures Collections.order works when the ordered column does not exist
    """
    collection.model.rank = None
    collection.order({'_order': 'rank'})
    assert collection._order == collection.model.id


def test_collection_order_none(collection):
    """
    Ensures Collections.order return None when there is no _order
    """
    collection.order({})
    assert collection._order is collection.model.id


def test_collection_apply_owner(magic):
    user = magic()
    payload = {}
    Collections.apply_owner(user, payload)
    assert payload == {'owner_id': user.id}


def test_collection_apply_owner_request(magic):
    user = magic()
    payload = {'owner_id': 1}
    Collections.apply_owner(user, payload)
    assert payload == {'owner_id': 1}


def test_collection_process_params(patch, collection):
    """
    Ensures Collection.process_params processes params.
    """
    patch.many(Collections, ['page', 'items', 'order', 'query'])
    collection.process_params('params')
    assert Collections.page.call_count == 1
    assert Collections.items.call_count == 1
    assert Collections.order.call_count == 1
    assert Collections.query.call_count == 1


def test_collection_get_data(collection, magic):
    """
    Ensures get_data can get the data.
    """
    user = magic()
    result = collection.get_data(user)
    user.do.assert_called_with('read', collection.model.q, collection.model)
    assert result == user.do()


def test_collection_paginate_data(collection, magic):
    """
    Ensures Collections.paginate_data can paginate the get_data
    """
    collection._page = 1
    collection._items = 20
    collection._order = 'order'
    data = magic()
    result = collection.paginate_data(data)
    data.order_by.assert_called_with('order')
    data.order_by().paginate.assert_called_with(1, 20)
    assert data.order_by().paginate().execute.call_count == 1
    assert result == list(data.order_by().paginate().execute())


def test_collection_on_get(patch, magic, collection, siren):
    patch.many(Collections, ['process_params', 'embeds', 'get_data',
                             'paginate_data'])
    collection._page = 'page'
    collection._items = 'items'
    request = magic()
    response = magic()
    user = magic()
    collection.on_get(request, response, user=user)
    Collections.process_params.assert_called_with(request.params)
    Collections.embeds.assert_called_with(request.params)
    Collections.get_data.assert_called_with(user)
    Collections.paginate_data.assert_called_with(Collections.get_data())
    args = (collection.model, Collections.paginate_data(), request.path)
    count = Collections.get_data().count()
    siren.__init__.assert_called_with(*args, page='page', total=count)
    siren.encode.assert_called_with(includes=Collections.embeds())
    assert response.body == siren().encode()


def test_collection_on_post(patch, magic, collection, siren):
    request = magic()
    response = magic()
    user = magic()
    patch.object(rapidjson, 'load')
    patch.object(Collections, 'apply_owner')
    collection.on_post(request, response, user=user)
    rapidjson.load.assert_called_with(request.bounded_stream)
    collection.apply_owner.assert_called_with(user, rapidjson.load())
    collection.model.create.assert_called_with(**rapidjson.load())
    siren.__init__.assert_called_with(collection.model,
                                      collection.model.create(),
                                      request.path)
    assert response.body == siren.encode()


def test_collection_on_patch(patch, magic, collection):
    request = magic()
    response = magic()
    collection.on_patch(request, response)
    assert response.status == HTTP_501
