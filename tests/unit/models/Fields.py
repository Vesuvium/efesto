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

from peewee import BooleanField, CharField, ForeignKeyField, IntegerField, SQL


def test_fields():
    assert Fields.field_type.default == 'string'
    assert isinstance(Fields.name, CharField)
    assert isinstance(Fields.field_type, CharField)
    assert isinstance(Fields.unique, BooleanField)
    assert Fields.unique.default is False
    assert Fields.unique.constraints == [SQL('DEFAULT false')]
    assert isinstance(Fields.nullable, BooleanField)
    assert Fields.nullable.default is False
    assert Fields.nullable.constraints == [SQL('DEFAULT false')]
    assert isinstance(Fields.default_value, IntegerField)
    assert Fields.default_value.null is True
    assert isinstance(Fields.type_id, ForeignKeyField)
    assert isinstance(Fields.owner, ForeignKeyField)
    assert issubclass(Fields, Base)
