# -*- coding: utf-8 -*-
from efesto.Api import Api
from efesto.App import App
from efesto.Blueprints import Blueprints
from efesto.Config import Config
from efesto.models import Base, Fields, Types, Users, db


def test_app_config(patch):
    patch.init(Config)
    assert isinstance(App.config(), Config)


def test_app_run(patch):
    patch.init(Api)
    patch.object(Api, 'start')
    patch.object(Base, 'init_db')
    patch.object(App, 'config')
    result = App.run()
    Base.init_db.assert_called_with(App.config().DB_URL)
    Api.__init__.assert_called_with(App.config())
    assert result == Api.start()


def test_app_install(patch, magic):
    patch.object(Base, 'init_db')
    patch.object(App, 'config')
    db.create_tables = magic()
    App.install()
    db.create_tables.assert_called_with([Fields, Types, Users])


def test_app_create_user(patch):
    patch.object(Base, 'init_db')
    patch.init(Users)
    patch.object(Users, 'save')
    patch.object(App, 'config')
    result = App.create_user('id', 'super')
    Base.init_db.assert_called_with(App.config().DB_URL)
    Users.__init__.assert_called_with(identifier='id', owner_permission=1,
                                      group_permission=1, others_permission=1,
                                      superuser='super')
    assert result == Users.save()


def test_app_load(patch):
    patch.object(Base, 'init_db')
    patch.init(Blueprints)
    patch.object(Blueprints, 'load')
    patch.object(App, 'config')
    result = App.load('file')
    Base.init_db.assert_called_with(App.config().DB_URL)
    assert Blueprints.__init__.call_count == 1
    Blueprints.load.assert_called_with('file')
    assert result == Blueprints.load()
