# -*- coding: utf-8 -*-
from efesto.models.Database import db


def test_db_fallback():
    assert db.database is None
    assert list(db.connect_params) == []
