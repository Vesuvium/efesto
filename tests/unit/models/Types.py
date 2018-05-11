# -*- coding: utf-8 -*-
from efesto.models import Base, Types

from peewee import CharField, ForeignKeyField


def test_types():
    assert isinstance(Types.name, CharField)
    assert isinstance(Types.owner, ForeignKeyField)
    assert issubclass(Types, Base)
