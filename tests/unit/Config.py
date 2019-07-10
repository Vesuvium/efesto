# -*- coding: utf-8 -*-
from bassoon import Bassoon

from efesto.Config import Config


def test_config():
    assert issubclass(Config, Bassoon)


def test_config_defaults():
    db_url = 'sqlite:///efesto.db'
    assert Config.defaults['ADMIN_ENDPOINTS'] == '0'
    assert Config.defaults['APP_NAME'] == 'efesto'
    assert Config.defaults['BATCH_ENDPOINTS'] == '1'
    assert Config.defaults['DB_URL'] == db_url
    assert Config.defaults['HATEOAS_ENCODER'] == 'siren'
    assert Config.defaults['JWT_SECRET'] == 'secret'
    assert Config.defaults['JWT_LEEWAY'] == '5'
    assert Config.defaults['JWT_AUDIENCE'] == 'efesto'
    assert Config.defaults['LOG_LEVEL'] == 'error'
    format = '[{time:YYYY-MM-DD HH:mm:ss}] [{level}] {message}'
    assert Config.defaults['LOG_FORMAT'] == format
    assert Config.defaults['PUBLIC_ENDPOINTS'] == 'index,version'
    assert Config.defaults['SWAGGER'] == '1'
    assert Config.defaults['XCLACKS'] == '1'
