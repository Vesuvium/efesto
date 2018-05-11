# -*- coding: utf-8 -*-
from efesto.models import Base, DynamicModel, Fields

from peewee import (BooleanField, CharField, DateTimeField, FloatField,
                    ForeignKeyField, IntegerField)

from pytest import mark


def test_mappings():
    assert DynamicModel.mappings['string'] == CharField
    assert DynamicModel.mappings['int'] == IntegerField
    assert DynamicModel.mappings['float'] == FloatField
    assert DynamicModel.mappings['bool'] == BooleanField
    assert DynamicModel.mappings['date'] == DateTimeField


def test_dynamic_model_init():
    model = DynamicModel()
    assert model.models == {}


@mark.parametrize('field_type, expected', [
    ('string', CharField),
    ('int', IntegerField),
    ('float', FloatField),
    ('bool', BooleanField),
    ('date', DateTimeField)
])
def test_dynamic_model_make_field(magic, field_type, expected):
    retrieved_field = magic(field_type=field_type)
    field = DynamicModel.make_field(retrieved_field)
    assert isinstance(field, expected)


def test_dynamic_model_make_field_not_found(magic):
    assert isinstance(DynamicModel.make_field(magic()), CharField)


def test_dynamic_model_make_field_nullable(magic):
    retrieved_field = magic(nullable=True)
    field = DynamicModel.make_field(retrieved_field)
    assert field.null is True


def test_dynamic_model_make_field_unique(magic):
    retrieved_field = magic(unique=True)
    field = DynamicModel.make_field(retrieved_field)
    assert field.unique is True


def test_dynamic_model_attributes(patch, magic):
    patch.object(DynamicModel, 'make_field')
    field = magic()
    field.name = 'one'
    result = DynamicModel.attributes([field])
    DynamicModel.make_field.assert_called_with(field)
    assert result['one'] == DynamicModel.make_field()


def test_dynamic_model_new_model(patch, magic):
    patch.object(DynamicModel, 'attributes', return_value={})
    patch.object(Fields, 'select')
    type_instance = magic()
    type_instance.name = 'custom'
    dynamicmodel = DynamicModel()
    dynamicmodel.generate(type_instance)
    Fields.select().where.assert_called_with(False)
    DynamicModel.attributes.assert_called_with(Fields.select().where())
    model = dynamicmodel.models['custom']
    assert isinstance(model.owner, ForeignKeyField)
    assert issubclass(model, Base)
    assert model.__name__ == 'custom'


def test_dynamic_model_generate(patch, magic):
    """
    Ensures that a model can be generated from a Type
    """
    patch.object(DynamicModel, 'attributes', return_value={})
    patch.object(Fields, 'select')
    type_instance = magic()
    type_instance.name = 'custom'
    dynamicmodel = DynamicModel()
    result = dynamicmodel.generate(type_instance)
    Fields.select().where.assert_called_with(False)
    DynamicModel.attributes.assert_called_with(Fields.select().where())
    assert isinstance(result.owner, ForeignKeyField)
    assert issubclass(result, Base)
    assert result.__name__ == 'custom'
    assert dynamicmodel.models['custom'] == result
