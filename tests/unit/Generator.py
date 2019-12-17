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
from efesto.Generator import Generator
from efesto.models import Fields

from psyker import Column, Foreign

from pytest import fixture


@fixture
def db(magic):
    return magic()


@fixture
def generator(db):
    generator = Generator(db)
    generator.models = {'custom': 'custom'}
    return generator


def test_mappings():
    assert Generator.mappings['string'] == 'str'
    assert Generator.mappings['text'] == 'text'
    assert Generator.mappings['int'] == 'int'
    assert Generator.mappings['bigint'] == 'bigint'
    assert Generator.mappings['float'] == 'float'
    assert Generator.mappings['double'] == 'double'
    assert Generator.mappings['decimal'] == 'decimal'
    assert Generator.mappings['boolean'] == 'bool'
    assert Generator.mappings['date'] == 'date'
    assert Generator.mappings['datetime'] == 'datetime'
    assert Generator.mappings['uuid'] == 'uuid'


def test_generator_init(db):
    result = Generator(db)
    assert result.db == db
    assert result.models == {}


def test_generator_make_field(patch, magic, generator):
    patch.init(Column)
    field = magic(field_type='string', default_value=None, length=None)
    field.name = 'name'
    result = generator.make_field(field)
    Column.__init__.assert_called_with('name', 'str', nullable=field.nullable,
                                       unique=field.unique)
    assert isinstance(result, Column)


def test_generator_make_field__foreign(patch, magic, generator):
    patch.init(Foreign)
    field = magic(field_type='custom', default_value=None, length=None)
    field.name = 'name'
    result = generator.make_field(field)
    Foreign.__init__.assert_called_with('name', field.field_type,
                                        nullable=field.nullable,
                                        unique=field.unique)
    assert isinstance(result, Foreign)


def test_generator_make_field__default_value(patch, magic, generator):
    patch.init(Column)
    field = magic(field_type='string', length=None)
    field.name = 'name'
    result = generator.make_field(field)
    Column.__init__.assert_called_with('name', 'str', nullable=field.nullable,
                                       unique=field.unique,
                                       default=field.default_value)
    assert isinstance(result, Column)


def test_generator_make_field__length(patch, magic, generator):
    patch.init(Column)
    field = magic(field_type='string', default_value=None)
    field.name = 'name'
    result = generator.make_field(field)
    Column.__init__.assert_called_with('name', 'str', nullable=field.nullable,
                                       unique=field.unique,
                                       options={'length': field.length})
    assert isinstance(result, Column)


def test_generator_make_fields(patch, magic, generator):
    patch.init(Foreign)
    patch.object(Generator, 'make_field')
    field = magic()
    field.name = 'name'
    result = generator.make_fields([field])
    Generator.make_field.assert_called_with(field)
    Foreign.__init__.assert_called_with('owner', 'users')
    assert result['name'] == Generator.make_field()
    assert isinstance(result['owner'], Foreign)


def test_generator_new_model(patch, type_instance, generator, db):
    patch.object(Generator, 'make_fields')
    patch.object(Fields, 'select')
    generator.generate(type_instance)
    Fields.select.assert_called_with(type_id=type_instance.id)
    Generator.make_fields.assert_called_with(Fields.select().get())
    db.make_model.assert_called_with(type_instance.name,
                                     Generator.make_fields())
    assert generator.models[type_instance.name] == db.make_model()


def test_generator_generate(patch, generator, type_instance):
    """
    Ensures that a model can be generated from a Type
    """
    patch.object(Generator, 'new_model')
    result = generator.generate(type_instance)
    Generator.new_model.assert_called_with(type_instance)
    assert result == generator.models[type_instance.name]
