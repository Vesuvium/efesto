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
from efesto.Api import Api
from efesto.Generator import Generator
from efesto.Routes import Routes
from efesto.handlers import Collections, Items
from efesto.middlewares import Authentication, Clacks, Db, Json, Log, Msgpack
from efesto.models import Types

import falcon

from pytest import fixture


@fixture
def api(patch, config):
    patch.init(Generator)
    return Api(config)


def test_api():
    assert Api.available_middlewares['authentication'] == Authentication
    assert Api.available_middlewares['clacks'] == Clacks
    assert Api.available_middlewares['db'] == Db
    assert Api.available_middlewares['json'] == Json
    assert Api.available_middlewares['log'] == Log
    assert Api.available_middlewares['msgpack'] == Msgpack


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
    patch.init(Json)
    patch.init(Log)
    config.MIDDLEWARES = 'json:log'
    result = api.middlewares()
    Json.__init__.assert_called_with(config)
    Log.__init__.assert_called_with(config)
    assert isinstance(result[0], Json)
    assert isinstance(result[1], Log)


def test_api_middlewares__not_available(api, config):
    config.MIDDLEWARES = 'pizza'
    assert api.middlewares() == []


def test_api_falcon(patch, api):
    patch.object(falcon, 'API')
    patch.object(Api, 'middlewares')
    result = api.falcon()
    falcon.API.assert_called_with(middleware=Api.middlewares())
    assert result == falcon.API()


def test_api_start(patch, api):
    patch.object(Types, 'select')
    patch.many(Api, ['falcon', 'custom_routes', 'routes', 'middlewares'])
    api.start()
    Api.custom_routes.assert_called_with(Types.select().get())
    Api.routes.assert_called_with(Routes.routes)
    assert api.api == Api.falcon()
