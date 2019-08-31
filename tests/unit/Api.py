# -*- coding: utf-8 -*-
from efesto.Api import Api
from efesto.Generator import Generator
from efesto.Routes import Routes
from efesto.handlers import Collections, Items
from efesto.middlewares import Authentication, Json, Log
from efesto.models import Types

import falcon

from pytest import fixture


@fixture
def api(patch, config):
    patch.init(Generator)
    return Api(config)


def test_api_init(api, config):
    assert api.config == config
    assert api.api is None
    assert isinstance(api.generator, Generator)


def test_api_add_route(magic, api):
    api.api = magic()
    api.add_route('route', 'handler')
    api.api.add_route.assert_called_with('route', 'handler')


def test_api_add_route__model(magic, api):
    handler = magic()
    api.api = magic()
    api.add_route('route', handler, 'model')
    handler.assert_called_with('model')
    api.api.add_route.assert_called_with('route', handler())


def test_api_add_routes(patch, api):
    patch.object(Api, 'add_route')
    api.add_routes((('endpoint', 'handler'), ))
    Api.add_route.assert_called_with('endpoint', 'handler')


def test_api_type_route(patch, api, type_instance):
    patch.object(Generator, 'generate')
    patch.object(Api, 'add_routes')
    api.type_route(type_instance)
    Generator.generate.assert_called_with(type_instance)
    Api.add_routes.assert_called_with((
        ('/custom', Collections, Generator.generate()),
        ('/custom/{id}', Items, Generator.generate())
    ))


def test_api_add_custom_route(patch, api):
    patch.object(Api, 'add_routes')
    api.add_custom_route('name', 'model')
    api.add_routes.assert_called_with((
        ('/name', Collections, 'model'), ('/name/{id}', Items, 'model')
    ))


def test_api_middlewares(patch, api, config):
    patch.init(Authentication)
    patch.init(Log)
    result = api.middlewares()
    Authentication.__init__.assert_called_with(config.JWT_SECRET,
                                               config.JWT_AUDIENCE,
                                               config.PUBLIC_ENDPOINTS)
    Log.__init__.assert_called_with(config.LOG_LEVEL, config.LOG_FORMAT)
    assert isinstance(result[0], Authentication)
    assert isinstance(result[1], Json)
    assert isinstance(result[2], Log)


def test_api_start(patch, magic, api):
    patch.object(falcon, 'API')
    patch.object(Types, 'select')
    patch.many(Api, ['type_route', 'add_routes', 'middlewares'])
    Types.select.return_value = magic(execute=magic(return_value=['type']))
    result = api.start()
    falcon.API.assert_called_with(middleware=Api.middlewares())
    Api.type_route.assert_called_with('type')
    Api.add_routes.assert_called_with(Routes.routes)
    assert result == api.api
