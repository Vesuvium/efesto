# -*- coding: utf-8 -*-
from efesto.Api import Api
from efesto.handlers import Collections, Items
from efesto.models import DynamicModel

import falcon

from pytest import fixture


@fixture
def api(patch):
    patch.object(falcon, 'API')
    return Api()


def test_api_init(patch):
    patch.object(falcon, 'API')
    api = Api()
    assert api.api == falcon.API()


def test_api_init_kwargs(patch):
    patch.object(falcon, 'API')
    Api(key='value')
    falcon.API.assert_called_with(key='value')


def test_api_collection(patch, magic, api):
    patch.init(Collections)
    model = magic()
    result = api.collection(model)
    Collections.__init__.assert_called_with(model)
    assert isinstance(result, Collections)


def test_api_item(patch, magic, api):
    patch.init(Items)
    model = magic()
    result = api.item(model)
    Items.__init__.assert_called_with(model)
    assert isinstance(result, Items)


def test_api_list_route(patch, magic, api):
    patch.object(api, 'collection')
    model = magic()
    api.list_route('/endpoint', model)
    api.collection.assert_called_with(model)
    api.api.add_route.assert_called_with('/endpoint', api.collection())


def test_api_object_route(patch, magic, api):
    patch.object(api, 'item')
    model = magic()
    api.object_route('/endpoint', model)
    api.item.assert_called_with(model)
    api.api.add_route.assert_called_with('/endpoint/{id}', api.item())


def test_api_add_endpoint(patch, magic, api):
    patch.many(Api, ['list_route', 'object_route'])
    model = magic()
    api.add_endpoint('/endpoint', model)
    api.list_route.assert_called_with('/endpoint', model)
    api.object_route.assert_called_with('/endpoint', model)


def test_api_dynamic_endpoints(patch, api, type_instance):
    patch.init(DynamicModel)
    patch.object(DynamicModel, 'generate')
    patch.object(Api, 'add_endpoint')
    api.dynamic_endpoints([type_instance])
    assert DynamicModel.__init__.call_count == 1
    DynamicModel.generate.assert_called_with(type_instance)
    api.add_endpoint.assert_called_with('/custom', DynamicModel.generate())


def test_api_cherries(api):
    assert api.cherries() == api.api
