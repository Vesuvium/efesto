# -*- coding: utf-8 -*-
from peewee import BooleanField, CharField, ForeignKeyField, IntegerField, SQL

from .Base import Base
from .Types import Types
from .Users import Users


class Fields(Base):
    name = CharField()
    field_type = CharField(default='string')
    unique = BooleanField(default=False, constraints=[SQL('DEFAULT false')])
    nullable = BooleanField(default=False, constraints=[SQL('DEFAULT false')])
    default_value = IntegerField(null=True)
    type_id = ForeignKeyField(Types)
    owner = ForeignKeyField(Users)
