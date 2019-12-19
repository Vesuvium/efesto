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
from efesto.models import Base, Types

from psyker import Foreign


def test_types():
    assert issubclass(Types, Base)


def test_types_columns(patch):
    patch.init(Foreign)
    patch.object(Types, 'permissions', return_value={'col': 'value'})
    columns = Types.columns()
    assert columns['name'] == 'str'
    assert isinstance(columns['owner'], Foreign)
    Foreign.__init__.assert_called_with('owner', 'users')
    assert columns['col'] == 'value'
