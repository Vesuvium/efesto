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
from psyker import Column, Foreign

from .models import Fields


class Generator:
    """
    A model generator that is used to generated dynamically defined models.
    """
    __slots__ = ('db', 'models')

    mappings = {
        'string': 'str',
        'text': 'text',
        'int': 'int',
        'bigint': 'bigint',
        'float': 'float',
        'double': 'double',
        'decimal': 'decimal',
        'boolean': 'bool',
        'date': 'date',
        'datetime': 'datetime',
        'uuid': 'uuid'
    }

    def __init__(self, db):
        self.db = db
        self.models = {}

    def make_field(self, field):
        arguments = {'nullable': field.nullable, 'unique': field.unique}
        if field.length:
            arguments['options'] = {'length': field.length}
        if field.default_value:
            arguments['default'] = field.default_value
        if field.field_type in self.models:
            return Foreign(field.name, field.field_type, **arguments)
        return Column(field.name, self.mappings[field.field_type], **arguments)

    def make_fields(self, fields):
        fields = {field.name: self.make_field(field) for field in fields}
        fields['owner'] = Foreign('owner', 'users')
        return fields

    def new_model(self, type_instance):
        fields = Fields.select(type_id=type_instance.id).get()
        columns = self.make_fields(fields)
        model = self.db.make_model(type_instance.name, columns)
        self.models[type_instance.name] = model

    def generate(self, type_instance):
        """
        Generate a model using a type
        """
        self.new_model(type_instance)
        return self.models[type_instance.name]
