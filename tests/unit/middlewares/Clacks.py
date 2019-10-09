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
from efesto.middlewares import Clacks


def test_clacks_init():
    assert Clacks('config')


def test_clacks_process_response(response):
    clacks = Clacks('config')
    clacks.process_response('request', response, 'resource', 'success')
    value = 'GNU Terry Pratchett'
    response.set_header.assert_called_with('X-Clacks-Overhead', value)
