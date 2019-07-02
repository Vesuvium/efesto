# -*- coding: utf-8 -*-
from bassoon import Bassoon

from efesto.Config import Config


def test_config():
    assert issubclass(Config, Bassoon)


def test_config_defaults():
    db_url = 'sqlite:///efesto.db'
    assert Config.defaults['db_url'] == db_url
    assert Config.defaults['jwt_secret'] == 'secret'
    assert Config.defaults['jwt_leeway'] == 5
    assert Config.defaults['jwt_audience'] == 'efesto'
