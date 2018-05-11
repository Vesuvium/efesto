# -*- coding: utf-8 -*-
from efesto.models import Base, DynamicModel, Fields

from peewee import (BooleanField, CharField, DateTimeField, FloatField,
                    ForeignKeyField, IntegerField)

from pytest import fixture, mark


@fixture
def dynamicmodel(magic):
    dynamicmodel = DynamicModel()
    dynamicmodel.models = magic()
    return dynamicmodel


@fixture
def type_instance(magic):
    type_instance = magic()
    type_instance.name = 'custom'
    return type_instance


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
def test_dynamic_model_make_field(magic, dynamicmodel, field_type, expected):
    retrieved_field = magic(field_type=field_type)
    field = dynamicmodel.make_field(retrieved_field)
    assert isinstance(field, expected)


def test_dynamic_model_make_field_custom(patch, magic, dynamicmodel):
    patch.init(ForeignKeyField)
    dynamicmodel.models = {'custom': magic()}
    retrieved_field = magic(field_type='custom')
    field = dynamicmodel.make_field(retrieved_field)
    ForeignKeyField.__init__.assert_called_with(dynamicmodel.models['custom'])
    assert isinstance(field, ForeignKeyField)


def test_dynamic_model_make_field_not_found(magic, dynamicmodel):
    assert isinstance(dynamicmodel.make_field(magic()), CharField)


def test_dynamic_model_make_field_nullable(magic, dynamicmodel):
    retrieved_field = magic(nullable=True)
    field = dynamicmodel.make_field(retrieved_field)
    assert field.null is True


def test_dynamic_model_make_field_unique(magic, dynamicmodel):
    retrieved_field = magic(unique=True)
    field = dynamicmodel.make_field(retrieved_field)
    assert field.unique is True


def test_dynamic_model_attributes(patch, magic):
    patch.object(DynamicModel, 'make_field')
    field = magic()
    field.name = 'one'
    result = DynamicModel.attributes([field])
    DynamicModel.make_field.assert_called_with(field)
    assert result['one'] == DynamicModel.make_field()


def test_dynamic_model_new_model(patch, type_instance):
    patch.object(DynamicModel, 'attributes', return_value={})
    patch.object(Fields, 'select')
    dynamicmodel = DynamicModel()
    dynamicmodel.generate(type_instance)
    Fields.select().where.assert_called_with(False)
    DynamicModel.attributes.assert_called_with(Fields.select().where())
    model = dynamicmodel.models['custom']
    assert isinstance(model.owner, ForeignKeyField)
    assert issubclass(model, Base)
    assert model.__name__ == 'custom'


def test_dynamic_model_generate(patch, dynamicmodel, type_instance):
    """
    Ensures that a model can be generated from a Type
    """
    patch.object(DynamicModel, 'new_model')
    result = dynamicmodel.generate(type_instance)
    DynamicModel.new_model.assert_called_with(type_instance)
    assert result == dynamicmodel.models[type_instance.name]
