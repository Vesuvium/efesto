# -*- coding: utf-8 -*-
from bassoon import Bassoon

from efesto.Config import Config


def test_config():
    assert issubclass(Config, Bassoon)


def test_config_defaults():
    db_url = 'sqlite:///efesto.db'
    assert Config.defaults['DB_URL'] == db_url
    assert Config.defaults['JWT_SECRET'] == 'secret'
    assert Config.defaults['JWT_LEEWAY'] == '5'
    assert Config.defaults['JWT_AUDIENCE'] == 'efesto'
