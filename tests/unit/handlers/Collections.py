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
    assert collection.order({'_order': 'column'}) == 'column'


def test_collection_order_none(collection):
    """
    Ensures Collections.order return None when there is no _order
    """
    assert collection.order({}) is None


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


def test_collection_get_data(collection, magic):
    """
    Ensures get_data can get the data.
    """
    collection._page = 1
    collection._items = 20
    user = magic()
    result = collection.get_data(user)
    user.do.assert_called_with('read', collection.model.q, collection.model)
    user.do().paginate.assert_called_with(1, 20)
    assert user.do().paginate().execute.call_count == 1
    assert result == list(user.do().paginate().execute())


def test_collection_on_get(patch, magic, collection, siren):
    request = magic()
    response = magic()
    user = magic()
    patch.many(Collections, ['query', 'page', 'items', 'embeds'])
    collection.on_get(request, response, user=user)
    Collections.page.assert_called_with(request.params)
    Collections.items.assert_called_with(request.params)
    Collections.query.assert_called_with(request.params)
    Collections.embeds.assert_called_with(request.params)
    user.do.assert_called_with('read', collection.model.q, collection.model)
    user.do().paginate.assert_called_with(Collections.page(),
                                          Collections.items())
    assert user.do().paginate().execute.call_count == 1
    siren.__init__.assert_called_with(collection.model,
                                      list(user.do().execute()),
                                      request.path, page=Collections.page(),
                                      total=user.do().count())
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
