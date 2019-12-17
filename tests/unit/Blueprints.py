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
import os

from efesto.Blueprints import Blueprints
from efesto.models import Fields, Types

from pytest import fixture, raises

from ruamel.yaml import YAML


@fixture
def blueprints(magic):
    blueprints = Blueprints()
    blueprints.yaml = magic()
    return blueprints


def test_blueprints_init(patch):
    patch.init(YAML)
    blueprint = Blueprints()
    YAML.__init__.assert_called_with(typ='safe')
    assert isinstance(blueprint.yaml, YAML)


def test_blueprints_make_field(patch, blueprints):
    patch.init(Fields)
    patch.object(Fields, 'save')
    blueprints.make_field('field', 1)
    Fields.__init__.assert_called_with(name='field', type_id=1, owner_id=1)
    assert Fields.save.call_count == 1


def test_blueprints_make_field_options(patch, blueprints):
    patch.init(Fields)
    patch.object(Fields, 'save')
    blueprints.make_field('field', 1, option='value')
    Fields.__init__.assert_called_with(name='field', type_id=1, owner_id=1,
                                       option='value')


def test_blueprints_load_field(patch, magic, blueprints):
    patch.object(Blueprints, 'make_field')
    new_type = magic()
    result = blueprints.load_field(new_type, 'field')
    blueprints.make_field.assert_called_with('field', new_type.id)
    assert result == blueprints.make_field()


def test_blueprints_load_field_complex(patch, magic, blueprints):
    patch.object(Blueprints, 'make_field')
    new_type = magic()
    result = blueprints.load_field(new_type, {'field': {'key': 'value'}})
    blueprints.make_field.assert_called_with('field', new_type.id, key='value')
    assert result == blueprints.make_field()


def test_blueprints_load_type(patch, blueprints):
    patch.init(Types)
    patch.object(Types, 'save')
    result = blueprints.load_type('table')
    Types.__init__.assert_called_with(name='table', owner_id=1)
    assert result == Types.save()


def test_blueprints_read(patch, blueprints):
    patch.object(os, 'path')
    patch.object(os, 'getcwd', return_value='cwd')
    result = blueprints.read('name.yml')
    assert os.getcwd.call_count == 1
    os.path.join.assert_called_with(os.getcwd(), 'name.yml')
    assert result == blueprints.yaml.load()


def test_blueprints_read_no_file(patch, blueprints):
    patch.object(os, 'path')
    os.path.isfile.return_value = False
    patch.object(os, 'getcwd', return_value='cwd')
    with raises(ValueError):
        blueprints.read('name.cfg')


def test_blueprints_parse(patch, blueprints):
    patch.many(Blueprints, ['load_type', 'load_field'])
    blueprints.parse({'types': {'type': ['field']}})
    blueprints.load_type.assert_called_with('type')
    blueprints.load_field.assert_called_with(blueprints.load_type(), 'field')


def test_blueprints_load(patch, blueprints):
    patch.many(Blueprints, ['read', 'parse'])
    blueprints.load('name.yml')
    Blueprints.read.assert_called_with('name.yml')
    Blueprints.parse.assert_called_with(blueprints.read())
