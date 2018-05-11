# -*- coding: utf-8 -*-
from peewee import CharField, ForeignKeyField

from .Base import Base
from .Users import Users


class Types(Base):
    name = CharField()
    owner = ForeignKeyField(Users)
