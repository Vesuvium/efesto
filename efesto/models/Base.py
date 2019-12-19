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
from psyker import Column, Model, Psyker


class Base(Model):

    conversions = {
        'int': 'number',
        'bigint': 'number',
        'double': 'number',
        'decimal': 'number',
        'float': 'number',
        'bool': 'number',
        'serial': 'number',
        'str': 'text',
        'text': 'text',
        'date': 'date',
        'datetime': 'datetime',
        'uuid': 'text',
        'foreign': 'text'
    }

    @classmethod
    def permissions(cls):
        return {
            'group': Column('group', 'int', default=1),
            'owner_permission': Column('owner_permission', 'int', default=3),
            'group_permission': Column('group_permission', 'int', default=0),
            'others_permission': Column('others_permission', 'int', default=0)
        }

    @classmethod
    def get_columns(cls):
        columns = cls.__table__.columns.values()
        return [
            {col.name: cls.conversions[col.field_type]} for col in columns
        ]

    @classmethod
    def init_db(cls, url, models, connections, timeout, **kwargs):
        psyker = Psyker()
        psyker.add_models(*models)
        psyker.start(url)
        return psyker

    @classmethod
    def filter(cls, key, value, operator):
        return cls.q.where(**{key: (operator, value)})

    @staticmethod
    def cast(value):
        if value == 'true':
            return True
        elif value == 'false':
            return False
        elif value == 'null':
            return None
        return value

    @classmethod
    def write(cls, **kwargs):
        return cls(**kwargs).save()

    @classmethod
    def edit(cls, id, **data):
        return cls.update(**data).where(id=id).execute()
