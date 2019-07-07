# -*- coding: utf-8 -*-
from efesto.Api import Api
from efesto.Generator import Generator
from efesto.handlers import Collections, Items, Version
from efesto.models import Fields, Types, Users

import falcon

from pytest import fixture


@fixture
def api(patch):
    patch.object(falcon, 'API')
    patch.init(Generator)
    return Api()


def test_api_routes():
    assert Api.routes['/fields'] == {'model': Fields, 'handler': Collections}
    assert Api.routes['/fields/{id}'] == {'model': Fields, 'handler': Items}
    assert Api.routes['/types'] == {'model': Types, 'handler': Collections}
    assert Api.routes['/types/{id}'] == {'model': Types, 'handler': Items}
    assert Api.routes['/users'] == {'model': Users, 'handler': Collections}
    assert Api.routes['/users/{id}'] == {'model': Users, 'handler': Items}
    assert Api.routes['/version'] == Version


def test_api_init(api):
    assert api.api == falcon.API()
    assert isinstance(api.generator, Generator)


def test_api_init_kwargs(patch):
    patch.object(falcon, 'API')
    patch.init(Generator)
    Api(key='value')
    falcon.API.assert_called_with(key='value')


def test_api_type_route(patch, api, type_instance):
    patch.object(Generator, 'generate')
    api.type_route(type_instance)
    Generator.generate.assert_called_with(type_instance)
    assert api.routes['/custom'] == {'model': Generator.generate(),
                                     'handler': Collections}
    assert api.routes['/custom/{id}'] == {'model': Generator.generate(),
                                          'handler': Items}


def test_api_add_endpoint(patch, api):
    api.add_endpoint('route', 'handler')
    api.api.add_route.assert_called_with('route', 'handler')


def test_api_add_endpoint_dict(patch, magic, api):
    handler = magic()
    api.add_endpoint('route', {'handler': handler, 'model': 'model'})
    handler.assert_called_with('model')
    api.api.add_route.assert_called_with('route', handler())


def test_api_start(patch, magic, api):
    patch.object(Types, 'select')
    patch.many(Api, ['type_route', 'add_endpoint'])
    Types.select.return_value = magic(execute=magic(return_value=['type']))
    api.routes = {'route': 'handler'}
    result = api.start()
    Api.type_route.assert_called_with('type')
    Api.add_endpoint.assert_called_with('route', 'handler')
    assert result == api.api
