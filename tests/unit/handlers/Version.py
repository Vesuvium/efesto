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
from efesto.Version import version
from efesto.handlers import Version


def test_version_on_get(response):
    Version.on_get('request', response)
    data = {'properties': {'version': version},
            'links': [{'href': '/version', 'rel': 'self'}],
            'class': ['Version']}
    assert response.body == data


def test_version_on_get__params(response):
    Version.on_get('request', response, user='user')
    data = {'properties': {'version': version},
            'links': [{'href': '/version', 'rel': 'self'}],
            'class': ['Version']}
    assert response.body == data
