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
from efesto.Siren import Siren
from efesto.exceptions import BadRequest
from efesto.handlers import BaseHandler, Collections

from falcon import HTTP_501

from pytest import fixture, raises


@fixture
def collection(magic):
    collection = Collections(magic())
    collection.q = magic()
    return collection


def test_collection():
    assert issubclass(Collections, BaseHandler)


def test_collection_query(collection):
    collection.query({})
    assert collection.model.q == collection.model.select().where()


def test_collection_query_params(collection):
    collection.query({'key': 'value'})
    collection.model.select().where.assert_called_with(key='value')


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
    collection.model.get_columns.return_value = ['col']
    collection.order({'_order': 'col'})
    assert collection._order == {'col': 'asc'}


def test_collection_order__desc(collection):
    """
    Ensures Collections.order allows descending queries
    """
    collection.model.get_columns.return_value = ['col']
    collection.order({'_order': '-col'})
    assert collection._order == {'col': 'desc'}


def test_collection_order_no_column(collection):
    """
    Ensures Collections.order works when the ordered column does not exist
    """
    collection.order({'_order': 'col'})
    assert collection._order == {'id': 'desc'}


def test_collection_order_none(collection):
    """
    Ensures Collections.order return None when there is no _order
    """
    collection.order({})
    assert collection._order == {'id': 'desc'}


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
    data = magic()
    result = collection.paginate_data(data)
    data.order_by.assert_called_with(**collection._order)
    data.order_by().paginate.assert_called_with(1, 20)
    assert result == data.order_by().paginate().dictionaries()


def test_collection_on_get(patch, magic, collection):
    patch.object(Siren, 'encode')
    patch.many(Collections, ['process_params', 'embeds', 'get_data',
                             'paginate_data'])
    collection._page = 'page'
    collection.model.__name__ = 'model'
    request = magic()
    response = magic()
    user = magic()
    collection.on_get(request, response, user=user)
    Collections.process_params.assert_called_with(request.params)
    Collections.embeds.assert_called_with(request.params)
    Collections.get_data.assert_called_with(user)
    Collections.paginate_data.assert_called_with(Collections.get_data())
    Siren.encode.assert_called_with(Collections.paginate_data(),
                                    Collections.embeds(), 'model',
                                    request.path, collection._page,
                                    collection.model.count().get())
    assert response.body == Siren.encode()


def test_collection_on_post(patch, magic, collection):
    patch.object(Siren, 'encode')
    patch.object(Collections, 'apply_owner')
    request = magic()
    response = magic()
    user = magic()
    collection.model.__name__ = 'model'
    collection.on_post(request, response, user=user)
    collection.apply_owner.assert_called_with(user, request.payload)
    collection.model.write.assert_called_with(**request.payload)
    Siren.encode.assert_called_with(collection.model.write().as_dictionary(),
                                    [], 'model', request.path)
    assert response.body == Siren.encode()


def test_collection_on_post__write_error(patch, magic, collection):
    patch.object(Collections, 'apply_owner')
    request = magic()
    response = magic()
    user = magic()
    collection.model.write.return_value = None
    with raises(BadRequest):
        collection.on_post(request, response, user=user)


def test_collection_on_patch(patch, magic, collection):
    request = magic()
    response = magic()
    collection.on_patch(request, response)
    assert response.status == HTTP_501
