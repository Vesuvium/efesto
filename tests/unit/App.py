# -*- coding: utf-8 -*-
from efesto.Api import Api
from efesto.App import App
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
