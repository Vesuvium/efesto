# -*- coding: utf-8 -*-
from peewee import (BigIntegerField, BooleanField, CharField, DateField,
                    DateTimeField, DecimalField, DoubleField, FloatField,
                    ForeignKeyField, IntegerField, SQL, TextField, UUIDField)

from .models import Base, Fields, Users


class Generator:
    """
    A model generator that is used to generated dynamically defined models.
    """

    mappings = {
        'string': CharField,
        'text': TextField,
        'int': IntegerField,
        'bigint': BigIntegerField,
        'float': FloatField,
        'double': DoubleField,
        'decimal': DecimalField,
        'boolean': BooleanField,
        'date': DateField,
        'datetime': DateTimeField,
        'uuid': UUIDField
    }

    def __init__(self):
        self.models = {}

    def field(self, field_type):
        """
        Finds the field to use, given a field type
        """
        if field_type in self.mappings:
            return self.mappings[field_type]
        elif field_type in self.models:
            return ForeignKeyField
        return CharField

    def make_field(self, field, classname):
        """
        Generates a field from a field row
        """
        custom_field = self.field(field.field_type)
        arguments = {'null': field.nullable, 'unique': field.unique}
        if custom_field == ForeignKeyField:
            arguments['backref'] = classname
            return custom_field(self.models[field.field_type], **arguments)
        if field.default_value:
            constraints = [SQL('DEFAULT {}'.format(field.default_value))]
            arguments['default'] = field.default_value
            arguments['constraints'] = constraints
        return custom_field(**arguments)

    def attributes(self, fields, classname):
        attributes = {}
        for field in fields:
            attributes[field.name] = self.make_field(field, classname)
        return attributes

    def new_model(self, type_instance):
        fields = Fields.select().where(Fields.type_id == type_instance.id)
        attributes = self.attributes(fields, type_instance.name)
        attributes['owner'] = ForeignKeyField(Users)
        model = type(type_instance.name, (Base, ), attributes)
        self.models[type_instance.name] = model

    def generate(self, type_instance):
        """
        Generate a model using a type
        """
        self.new_model(type_instance)
        return self.models[type_instance.name]
