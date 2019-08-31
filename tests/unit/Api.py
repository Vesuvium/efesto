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


def test_api_route(magic, api):
    api.api = magic()
    api.route('route', 'handler')
    api.api.add_route.assert_called_with('route', 'handler')


def test_api_route__model(magic, api):
    handler = magic()
    api.api = magic()
    api.route('route', handler, 'model')
    handler.assert_called_with('model')
    api.api.add_route.assert_called_with('route', handler())


def test_api_routes(patch, api):
    patch.object(Api, 'route')
    api.routes((('endpoint', 'handler'), ))
    Api.route.assert_called_with('endpoint', 'handler')


def test_api_custom_route(patch, api):
    patch.object(Api, 'routes')
    api.custom_route('name', 'model')
    api.routes.assert_called_with((
        ('/name', Collections, 'model'), ('/name/{id}', Items, 'model')
    ))


def test_api_custom_routes(patch, api, type_instance):
    patch.object(Generator, 'generate')
    patch.object(Api, 'custom_route')
    api.custom_routes((type_instance, ))
    Generator.generate.assert_called_with(type_instance)
    Api.custom_route.assert_called_with(type_instance.name,
                                        Generator.generate())


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
    patch.many(Api, ['custom_routes', 'routes', 'middlewares'])
    result = api.start()
    falcon.API.assert_called_with(middleware=Api.middlewares())
    Api.custom_routes.assert_called_with(Types.select().execute())
    Api.routes.assert_called_with(Routes.routes)
    assert result == api.api
