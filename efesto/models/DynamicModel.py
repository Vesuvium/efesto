# -*- coding: utf-8 -*-
from peewee import (BooleanField, CharField, DateTimeField, FloatField,
                    ForeignKeyField, IntegerField)

from .Base import Base
from .Fields import Fields
from .Users import Users


class DynamicModel:

    mappings = {
        'string': CharField,
        'int': IntegerField,
        'float': FloatField,
        'bool': BooleanField,
        'date': DateTimeField
    }

    @classmethod
    def make_field(cls, field):
        custom_field = CharField
        if field.field_type in cls.mappings:
            custom_field = cls.mappings[field.field_type]
        return custom_field(null=field.nullable, unique=field.unique)

    @classmethod
    def attributes(cls, fields):
        attributes = {}
        for field in fields:
            attributes[field.name] = cls.make_field(field)
        return attributes

    @classmethod
    def generate(cls, type_instance):
        """
        Generate a model using a type
        """
        fields = Fields.select().where(Fields.type_id == type_instance.id)
        attributes = cls.attributes(fields)
        attributes['owner'] = ForeignKeyField(Users)
        return type(type_instance.name, (Base, ), attributes)
