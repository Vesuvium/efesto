# -*- coding: utf-8 -*-
from efesto.Api import Api
from efesto.Generator import Generator
from efesto.handlers import Collections, Items, Version
from efesto.middlewares import Authentication
from efesto.models import Fields, Types, Users

import falcon

from pytest import fixture


@fixture
def api(patch, config):
    patch.init(Generator)
    return Api(config)


def test_api_routes():
    assert Api.routes['/fields'] == {'model': Fields, 'handler': Collections}
    assert Api.routes['/fields/{id}'] == {'model': Fields, 'handler': Items}
    assert Api.routes['/types'] == {'model': Types, 'handler': Collections}
    assert Api.routes['/types/{id}'] == {'model': Types, 'handler': Items}
    assert Api.routes['/users'] == {'model': Users, 'handler': Collections}
    assert Api.routes['/users/{id}'] == {'model': Users, 'handler': Items}
    assert Api.routes['/version'] == Version


def test_api_init(api, config):
    assert api.config == config
    assert api.api is None
    assert isinstance(api.generator, Generator)


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


def test_api_middlewares(patch, api, config):
    patch.init(Authentication)
    result = api.middlewares()
    Authentication.__init__.assert_called_with(config.JWT_SECRET,
                                               config.JWT_AUDIENCE)
    assert isinstance(result[0], Authentication)


def test_api_start(patch, magic, api):
    patch.object(Types, 'select')
    patch.many(Api, ['type_route', 'add_endpoint'])
    Types.select.return_value = magic(execute=magic(return_value=['type']))
    api.routes = {'route': 'handler'}
    result = api.start()
    Api.type_route.assert_called_with('type')
    Api.add_endpoint.assert_called_with('route', 'handler')
    assert result == api.api
