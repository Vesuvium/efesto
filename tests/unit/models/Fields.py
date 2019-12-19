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
from efesto.models import Base, Fields

from psyker import Column, Foreign


def test_fields():
    assert issubclass(Fields, Base)


def test_fields_columns(patch):
    patch.object(Fields, 'permissions', return_value={'col': 'value'})
    result = Fields.columns()
    assert result['name'] == 'str'
    assert result['length'] == 'int'
    assert result['default_value'] == 'int'
    assert isinstance(result['field_type'], Column)
    assert isinstance(result['unique'], Column)
    assert isinstance(result['nullable'], Column)
    assert isinstance(result['type_id'], Foreign)
    assert isinstance(result['owner'], Foreign)
    assert result['col'] == 'value'
