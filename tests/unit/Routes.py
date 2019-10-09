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
