# -*- coding: utf-8 -*-
from efesto.Routes import Routes
from efesto.handlers import Collections, Items, Version
from efesto.models import Fields, Types, Users


def test_routes_routes():
    assert Routes.routes[0] == ('/fields', Collections, Fields)
    assert Routes.routes[1] == ('/fields/{id}', Items, Fields)
    assert Routes.routes[2] == ('/types', Collections, Types)
    assert Routes.routes[3] == ('/types/{id}', Items, Types)
    assert Routes.routes[4] == ('/users', Collections, Users)
    assert Routes.routes[5] == ('/users/{id}', Items, Users)
    assert Routes.routes[6] == ('/version', Version)
