# -*- coding: utf-8 -*-
from efesto.Siren import Siren
from efesto.handlers import Collections

from falcon import HTTP_501

from pytest import fixture

import ujson


@fixture
def collection(magic):
    return Collections(magic())


def test_collection_init():
    collection = Collections('model')
    assert collection.model == 'model'


def test_collection_query(collection):
    result = collection.query({})
    assert collection.model.select.call_count == 1
    assert result == collection.model.q


def test_collection_query_params(collection):
    collection.query({'key': 'value'})
    collection.model.query.assert_called_with('key', 'value')


def test_collection_page(collection):
    assert collection.page({'page': '2'}) == 2


def test_collection_page_none(collection):
    assert collection.page({}) == 1


def test_collection_items(collection):
    assert collection.items({'items': '2'}) == 2


def test_collection_items_none(collection):
    assert collection.items({}) == 20


def test_collection_on_get(patch, magic, collection):
    request = magic()
    response = magic()
    user = magic()
    patch.init(Siren)
    patch.object(Siren, 'encode')
    patch.many(Collections, ['query', 'page', 'items'])
    collection.on_get(request, response, user=user)
    Collections.page.assert_called_with(request.params)
    Collections.items.assert_called_with(request.params)
    Collections.query.assert_called_with(request.params)
    user.do.assert_called_with('read', collection.query(),
                               collection.model)
    user.do().paginate.assert_called_with(Collections.page(),
                                          Collections.items())
    assert user.do().paginate().execute.call_count == 1
    Siren.__init__.assert_called_with(collection.model,
                                      list(user.do().execute()),
                                      request.path, page=Collections.page(),
                                      total=user.do().count())
    assert response.body == Siren().encode()


def test_collection_on_post(patch, magic, collection):
    request = magic()
    response = magic()
    user = magic()
    patch.init(Siren)
    patch.object(Siren, 'encode')
    patch.object(ujson, 'load')
    collection.on_post(request, response, user=user)
    ujson.load.assert_called_with(request.bounded_stream)
    collection.model.create.assert_called_with(owner_id=user.id,
                                               **ujson.load())
    Siren.__init__.assert_called_with(collection.model,
                                      collection.model.create(),
                                      request.path)
    assert response.body == Siren.encode()


def test_collection_on_patch(patch, magic, collection):
    request = magic()
    response = magic()
    collection.on_patch(request, response)
    assert response.status == HTTP_501
