# -*- coding: utf-8 -*-
from efesto.Api import Api
from efesto.App import App
from efesto.Blueprints import Blueprints
from efesto.Config import Config
from efesto.Generator import Generator
from efesto.models import Base, Fields, Types, Users, db

from peewee import IntegrityError


def test_app_config(patch):
    patch.init(Config)
    assert isinstance(App.config(), Config)


def test_app_generator(patch):
    patch.init(Generator)
    assert isinstance(App.generator(), Generator)


def test_app_init(patch):
    patch.object(Base, 'init_db')
    patch.object(App, 'config')
    result = App.init()
    Base.init_db.assert_called_with(App.config().DB_URL,
                                    App.config().DB_CONNECTIONS,
                                    App.config().DB_TIMEOUT)
    assert result == App.config()


def test_app_run(patch):
    patch.init(Api)
    patch.object(Api, 'start')
    patch.object(App, 'init')
    result = App.run()
    Api.__init__.assert_called_with(App.init())
    assert result == Api.start()


def test_app_install(patch, magic):
    patch.object(App, 'init')
    db.create_tables = magic()
    App.install()
    assert App.init.call_count == 1
    db.create_tables.assert_called_with([Fields, Types, Users])


def test_app_create_user(patch):
    patch.init(Users)
    patch.object(Users, 'save')
    patch.object(App, 'init')
    result = App.create_user('id', 'super')
    assert App.init.call_count == 1
    Users.__init__.assert_called_with(identifier='id', owner_permission=1,
                                      group_permission=1, others_permission=1,
                                      superuser='super')
    assert result == Users.save()


def test_app_create_user__error(patch):
    patch.init(Users)
    patch.object(Users, 'save', side_effect=IntegrityError)
    patch.object(App, 'init')
    assert App.create_user('id', 'super') is None


def test_app_load(patch, magic):
    patch.init(Blueprints)
    patch.object(Blueprints, 'load')
    patch.init(Generator)
    patch.object(Generator, 'generate')
    patch.object(Types, 'select')
    patch.many(App, ['init', 'generator'])
    db.create_tables = magic()
    Types.select().execute.return_value = ['type']
    App.load('file')
    assert App.init.call_count == 1
    assert Blueprints.__init__.call_count == 1
    Blueprints.load.assert_called_with('file')
    App.generator().generate.assert_called_with('type')
    db.create_tables.assert_called_with(App.generator().models.values(),
                                        safe=True)
