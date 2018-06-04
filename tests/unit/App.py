# -*- coding: utf-8 -*-
from efesto.Api import Api
from efesto.App import App
from efesto.Middlewares import Authentication
from efesto.models import Base, Types


def test_app_run(patch):
    patch.init(Api)
    patch.init(Authentication)
    patch.many(Api, ['cherries', 'add_endpoint', 'dynamic_endpoints'])
    patch.object(Base, 'init_db')
    patch.object(Types, 'select')
    url = 'postgres://postgres:postgres@localhost:5432/efesto'
    result = App.run()
    Base.init_db.assert_called_with(url)
    Authentication.__init__.assert_called_with('secret', 'efesto')
    assert Api.__init__.call_count == 1
    assert Api.add_endpoint.call_count == 3
    assert Types.select.call_count == 1
    Api.dynamic_endpoints.assert_called_with(Types.select().execute())
    assert result == Api.cherries()
