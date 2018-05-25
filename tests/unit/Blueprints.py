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


def test_blueprints_init():
    blueprint = Blueprints()
    assert isinstance(blueprint.yaml, YAML)


def test_blueprints_make_field(patch, blueprints):
    patch.object(Fields, 'create')
    blueprints.make_field('field', 1)
    Fields.create.assert_called_with(name='field', type_id=1, owner_id=1)
    assert Fields.create().save.call_count == 1


def test_blueprints_make_field_options(patch, blueprints):
    patch.object(Fields, 'create')
    blueprints.make_field('field', 1, option='value')
    Fields.create.assert_called_with(name='field', type_id=1, owner_id=1,
                                     option='value')


def test_blueprints_options(blueprints):
    result = blueprints.options([{'option': 'value'}])
    assert result['option'] == 'value'


def test_blueprints_load_field(patch, magic, blueprints):
    patch.object(Blueprints, 'make_field')
    new_type = magic()
    result = blueprints.load_field(new_type, 'field')
    blueprints.make_field.assert_called_with('field', new_type.id)
    assert result == blueprints.make_field()


def test_blueprints_load_field_complex(patch, magic, blueprints):
    patch.many(Blueprints, ['make_field', 'options'])
    new_type = magic()
    result = blueprints.load_field(new_type, {'field': 'options'})
    blueprints.options.assert_called_with('options')
    blueprints.make_field.assert_called_with('field', new_type.id,
                                             **blueprints.options())
    assert result == blueprints.make_field()


def test_blueprints_load_type(patch, blueprints):
    patch.object(Types, 'create')
    result = blueprints.load_type('table')
    Types.create.assert_called_with(name='table', owner_id=1)
    assert result == Types.create()


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
    blueprints.parse({'table': ['field']})
    blueprints.load_type.assert_called_with('table')
    blueprints.load_field.assert_called_with(blueprints.load_type(), 'field')


def test_blueprints_load(patch, blueprints):
    patch.many(Blueprints, ['read', 'parse'])
    blueprints.load('name.yml')
    Blueprints.read.assert_called_with('name.yml')
    Blueprints.parse.assert_called_with(blueprints.read())
