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


def test_blueprints_field_type(magic, blueprints):
    field = magic()
    blueprints.field_type('section.field', field)
    blueprints.parser.get.assert_called_with('section.field', 'type')
    assert field.field_type == blueprints.parser.get()


def test_blueprints_field_unique(magic, blueprints):
    field = magic()
    blueprints.field_unique('section.field', field)
    blueprints.parser.getboolean.assert_called_with('section.field', 'unique',
                                                    fallback=False)
    assert field.unique == blueprints.parser.getboolean()


def test_blueprints_field_nullable(magic, blueprints):
    field = magic()
    blueprints.field_nullable('section.field', field)
    blueprints.parser.getboolean.assert_called_with('section.field',
                                                    'nullable', fallback=False)
    assert field.nullable == blueprints.parser.getboolean()


def test_blueprints_load_field(patch, magic, blueprints):
    patch.object(Fields, 'create')
    patch.many(Blueprints, ['field_type', 'field_unique', 'field_nullable'])
    new_type = magic()
    blueprints.load_field('section', 'field', new_type)
    Fields.create.assert_called_with(name='field', type_id=new_type.id,
                                     owner_id=1)
    blueprints.parser.has_section.assert_called_with('section.field')
    Blueprints.field_type.assert_called_with('section.field', Fields.create())
    Blueprints.field_unique.assert_called_with('section.field',
                                               Fields.create())
    Blueprints.field_nullable.assert_called_with('section.field',
                                                 Fields.create())
    assert Fields.create().save.call_count == 1


def test_blueprints_section_fields(magic, blueprints):
    section = magic()
    result = blueprints.section_fields(section)
    blueprints.parser.has_option.assert_called_with(section, 'fields')
    blueprints.parser.get.assert_called_with(section, 'fields')
    assert result == blueprints.parser.get()


def test_blueprints_load_type(patch, blueprints):
    patch.object(Types, 'create')
    result = blueprints.load_type('section')
    Types.create.assert_called_with(name='section', owner_id=1)
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
    patch.many(Blueprints, ['load_type', 'section_fields', 'load_field'])
    Blueprints.section_fields.return_value = 'field '
    blueprints.parser.sections.return_value = ['section']
    blueprints.parse()
    Blueprints.load_type.assert_called_with('section')
    Blueprints.section_fields.assert_called_with('section')
    Blueprints.load_field.assert_called_with('section', 'field',
                                             Blueprints.load_type())


def test_blueprints_parse_ignore_dot(patch, blueprints):
    patch.object(Blueprints, 'load_type')
    blueprints.parser.sections.return_value = ['section.field']
    blueprints.parse()
    assert Blueprints.load_type.call_count == 0


def test_blueprints_load(patch, blueprints):
    patch.many(Blueprints, ['read', 'parse'])
    blueprints.load('name.cfg')
    Blueprints.read.assert_called_with('name.cfg')
    assert Blueprints.parse.call_count == 1
