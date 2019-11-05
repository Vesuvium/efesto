#   Copyright (C) 2018  Jacopo Cascioli
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
# -*- coding: utf-8 -*-
from peewee import (BigIntegerField, BooleanField, CharField, DateField,
                    DateTimeField, DecimalField, DoubleField, FloatField,
                    ForeignKeyField, IntegerField, SQL, TextField, UUIDField)

from .models import Base, Fields, Users


class Generator:
    """
    A model generator that is used to generated dynamically defined models.
    """
    __slots__ = ('models',)

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
        if field.length:
            arguments['max_length'] = field.length
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
