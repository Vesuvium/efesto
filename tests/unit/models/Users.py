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
from efesto.models import Base, Users

from psyker import Column


def test_users():
    assert issubclass(Users, Base)


def test_users_columns(patch):
    patch.init(Column)
    patch.object(Users, 'permissions', return_value={'col': 'value'})
    result = Users.columns()
    Column.__init__.assert_called_with('identifier', 'str', unique=True)
    assert isinstance(result['identifier'], Column)
    assert result['superuser'] == 'bool'
    assert result['col'] == 'value'


def test_users_do(patch):
    user = Users(superuser=False)
    assert user.do('action', 'query', 'model') is None


def test_users_do__superuser(patch):
    user = Users(superuser=True)
    assert user.do('action', 'query', 'model') == 'query'
