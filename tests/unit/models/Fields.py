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
