# -*- coding: utf-8 -*-
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


def test_collections_embeds(collection):
    result = collection.embeds({'_embeds': 'one'})
    model = collection.model
    collection.model.q.join.assert_called_with(model.one.rel_model, on=False)
    assert result == ['one']


def test_collections_embeds_none(collection):
    result = collection.embeds({'_embeds': None})
    assert result == []


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
    user.do.assert_called_with('read', collection.query(),
                               collection.model)
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
    patch.object(ujson, 'load')
    patch.object(Collections, 'apply_owner')
    collection.on_post(request, response, user=user)
    ujson.load.assert_called_with(request.bounded_stream)
    collection.apply_owner.assert_called_with(user, ujson.load())
    collection.model.create.assert_called_with(**ujson.load())
    siren.__init__.assert_called_with(collection.model,
                                      collection.model.create(),
                                      request.path)
    assert response.body == siren.encode()


def test_collection_on_patch(patch, magic, collection):
    request = magic()
    response = magic()
    collection.on_patch(request, response)
    assert response.status == HTTP_501
