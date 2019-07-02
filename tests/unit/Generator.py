# -*- coding: utf-8 -*-
from efesto.Generator import Generator
from efesto.models import Base, Fields

from peewee import (BigIntegerField, BooleanField, CharField, DateField,
                    DateTimeField, DecimalField, DoubleField, FloatField,
                    ForeignKeyField, IntegerField, SQL, TextField, UUIDField)

from pytest import fixture


@fixture
def generator(magic):
    generator = Generator()
    generator.models = magic()
    return generator


def test_mappings():
    assert Generator.mappings['string'] == CharField
    assert Generator.mappings['text'] == TextField
    assert Generator.mappings['int'] == IntegerField
    assert Generator.mappings['bigint'] == BigIntegerField
    assert Generator.mappings['float'] == FloatField
    assert Generator.mappings['double'] == DoubleField
    assert Generator.mappings['decimal'] == DecimalField
    assert Generator.mappings['boolean'] == BooleanField
    assert Generator.mappings['date'] == DateField
    assert Generator.mappings['datetime'] == DateTimeField
    assert Generator.mappings['uuid'] == UUIDField


def test_generator_init():
    model = Generator()
    assert model.models == {}


def test_generator_field(generator):
    assert generator.field('unknown') == CharField


def test_generator_field_from_mappings(generator):
    generator.mappings = {'type': 'class'}
    assert generator.field('type') == 'class'


def test_generator_field_from_models(generator):
    generator.models = {'type': 'model'}
    assert generator.field('type') == ForeignKeyField


def test_generator_make_field(patch, magic, generator):
    patch.object(Generator, 'field')
    field = magic(default_value=None)
    result = generator.make_field(field, 'classname')
    Generator.field.assert_called_with(field.field_type)
    Generator.field().assert_called_with(null=field.nullable,
                                         unique=field.unique)
    assert result == Generator.field()()


def test_generator_make_field_foreign(patch, magic, generator):
    patch.init(ForeignKeyField)
    patch.object(Generator, 'field', return_value=ForeignKeyField)
    field = magic(default_value=None)
    result = generator.make_field(field, 'classname')
    model = generator.models[field.field_type]
    ForeignKeyField.__init__.assert_called_with(model, null=field.nullable,
                                                unique=field.unique,
                                                backref='classname')
    assert isinstance(result, ForeignKeyField)


def test_generator_make_field_default_value(patch, magic, generator):
    patch.init(SQL)
    patch.object(Generator, 'field')
    field = magic(default_value='value')
    generator.make_field(field, 'classname')
    SQL.__init__.assert_called_with('DEFAULT value')
    kwargs = {'null': field.nullable, 'unique': field.unique,
              'default': field.default_value, 'constraints': [SQL()]}
    Generator.field().assert_called_with(**kwargs)


def test_generator_attributes(patch, magic, generator):
    patch.object(Generator, 'make_field')
    field = magic()
    field.name = 'one'
    result = generator.attributes([field], 'classname')
    Generator.make_field.assert_called_with(field, 'classname')
    assert result['one'] == generator.make_field()


def test_generator_new_model(patch, type_instance):
    patch.object(Generator, 'attributes', return_value={})
    patch.object(Fields, 'select')
    model = Generator()
    model.generate(type_instance)
    Fields.select().where.assert_called_with(False)
    Generator.attributes.assert_called_with(Fields.select().where(), 'custom')
    model = model.models['custom']
    assert isinstance(model.owner, ForeignKeyField)
    assert issubclass(model, Base)
    assert model.__name__ == 'custom'


def test_generator_generate(patch, generator, type_instance):
    """
    Ensures that a model can be generated from a Type
    """
    patch.object(Generator, 'new_model')
    result = generator.generate(type_instance)
    Generator.new_model.assert_called_with(type_instance)
    assert result == generator.models[type_instance.name]
