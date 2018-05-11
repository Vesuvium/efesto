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

    def __init__(self):
        self.models = {}

    def make_field(self, field):
        custom_field = CharField
        if field.field_type in self.mappings:
            custom_field = self.mappings[field.field_type]
        elif field.field_type in self.models:
            return ForeignKeyField(self.models[field.field_type])
        return custom_field(null=field.nullable, unique=field.unique)

    def attributes(self, fields):
        attributes = {}
        for field in fields:
            attributes[field.name] = self.make_field(field)
        return attributes

    def new_model(self, type_instance):
        fields = Fields.select().where(Fields.type_id == type_instance.id)
        attributes = self.attributes(fields)
        attributes['owner'] = ForeignKeyField(Users)
        model = type(type_instance.name, (Base, ), attributes)
        self.models[type_instance.name] = model

    def generate(self, type_instance):
        """
        Generate a model using a type
        """
        self.new_model(type_instance)
        return self.models[type_instance.name]
