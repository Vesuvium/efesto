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
from efesto.App import App
from efesto.Blueprints import Blueprints
from efesto.Config import Config
from efesto.Generator import Generator
from efesto.models import Base, Fields, Types, Users


def test_app_config(patch):
    patch.init(Config)
    assert isinstance(App.config(), Config)


def test_app_generator(patch):
    patch.init(Generator)
    result = App.generator('db')
    Generator.__init__.assert_called_with('db')
    assert isinstance(result, Generator)


def test_app_db(patch, config):
    patch.object(Base, 'init_db')
    result = App.db(config)
    Base.init_db.assert_called_with(config.DB_URL, (Users, Types, Fields),
                                    config.DB_CONNECTIONS, config.DB_TIMEOUT)
    assert result == Base.init_db()


def test_app_init(patch):
    patch.many(App, ['config', 'db'])
    result = App.init()
    App.db.assert_called_with(App.config())
    assert result == App.db()


def test_app_run(patch):
    patch.init(Api)
    patch.object(Api, 'start')
    patch.many(App, ['config', 'db'])
    result = App.run()
    App.db.assert_called_with(App.config())
    Api.__init__.assert_called_with(App.config(), App.db())
    assert result == Api.start()


def test_app_install(patch, magic):
    patch.object(App, 'init')
    App.install()
    assert App.init.call_count == 1


def test_app_create_user(patch):
    patch.init(Users)
    patch.object(Users, 'save')
    patch.object(App, 'init')
    result = App.create_user('id', 'super')
    assert App.init.call_count == 1
    Users.__init__.assert_called_with(identifier='id', owner_permission=1,
                                      group_permission=1, others_permission=1,
                                      superuser='super', group=1)
    assert result == Users.save()


def test_app_load(patch, magic):
    patch.init(Blueprints)
    patch.object(Blueprints, 'load')
    patch.init(Generator)
    patch.object(Generator, 'generate')
    patch.object(Types, 'select')
    patch.many(App, ['init', 'generator'])
    Types.select().get.return_value = ['type']
    App.load('file')
    assert Blueprints.__init__.call_count == 1
    Blueprints.load.assert_called_with('file')
    App.generator.assert_called_with(App.init())
    App.generator().generate.assert_called_with('type')
