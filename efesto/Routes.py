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
from .handlers import Collections, Items, Version
from .models import Fields, Types, Users


class Routes:
    __slots__ = ()

    routes = (
        ('/fields', Collections, Fields),
        ('/fields/{id}', Items, Fields),
        ('/types', Collections, Types),
        ('/types/{id}', Items, Types),
        ('/users', Collections, Users),
        ('/users/{id}', Items, Users),
        ('/version', Version)
    )
