# -*- coding: utf-8 -*-
from efesto.models.BaseModel import db


def test_db_fallback():
    assert db.database is None
    assert list(db.connect_kwargs.values()) == [None, None, None]
