# -*- coding: utf-8 -*-
from efesto.models import Proxy, db


def test_db():
    assert isinstance(db, Proxy)
