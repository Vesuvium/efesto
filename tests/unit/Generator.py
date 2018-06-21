# -*- coding: utf-8 -*-
from efesto.Generator import Generator
from efesto.models import Base, Fields

from peewee import (BooleanField, CharField, DateTimeField, FloatField,
                    ForeignKeyField, IntegerField, SQL, TextField)

from pytest import fixture, mark


@fixture
def generator(magic):
    generator = Generator()
    generator.models = magic()
    return generator


def test_mappings():
    assert Generator.mappings['string'] == CharField
    assert Generator.mappings['text'] == TextField
    assert Generator.mappings['int'] == IntegerField
    assert Generator.mappings['float'] == FloatField
    assert Generator.mappings['boolean'] == BooleanField
    assert Generator.mappings['date'] == DateTimeField


def test_generator_init():
    model = Generator()
    assert model.models == {}


@mark.parametrize('field_type, expected', [
    ('string', CharField),
    ('int', IntegerField),
    ('float', FloatField),
    ('boolean', BooleanField),
    ('date', DateTimeField)
])
def test_generator_make_field(magic, generator, field_type, expected):
    retrieved_field = magic(field_type=field_type, default_value=None)
    field = generator.make_field(retrieved_field)
    assert isinstance(field, expected)


def test_generator_make_field_custom(patch, magic, generator):
    patch.init(ForeignKeyField)
    generator.models = {'custom': magic()}
    retrieved_field = magic(field_type='custom', default_value=None)
    field = generator.make_field(retrieved_field)
    ForeignKeyField.__init__.assert_called_with(generator.models['custom'])
    assert isinstance(field, ForeignKeyField)


def test_generator_make_field_not_found(magic, generator):
    assert isinstance(generator.make_field(magic()), CharField)


def test_generator_make_field_nullable(magic, generator):
    retrieved_field = magic(nullable=True, default_value=None)
    field = generator.make_field(retrieved_field)
    assert field.null is True


def test_generator_make_field_unique(magic, generator):
    retrieved_field = magic(unique=True, default_value=None)
    field = generator.make_field(retrieved_field)
    assert field.unique is True


def test_generator_make_field_default_value(magic, generator):
    retrieved_field = magic(default_value=0)
    field = generator.make_field(retrieved_field)
    assert field.default == 0
    assert field.constraints == [SQL('DEFAULT 0')]


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
