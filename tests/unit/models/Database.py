# -*- coding: utf-8 -*-
from efesto.models import db

from peewee import PostgresqlDatabase


def test_db():
    assert isinstance(db, PostgresqlDatabase)
