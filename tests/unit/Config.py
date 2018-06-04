# -*- coding: utf-8 -*-
import os

from efesto.Config import Config

from pytest import fixture


@fixture
def init(patch):
    patch.object(Config, '__init__', return_value=None)


@fixture
def config():
    return Config()


def test_config():
    db_url = 'postgres://postgres:postgres@localhost:5432/efesto'
    assert Config.defaults['db_url'] == db_url
    assert Config.defaults['jwt_secret'] == 'secret'
    assert Config.defaults['jwt_leeway'] == 5
    assert Config.defaults['jwt_audience'] == 'efesto'


def test_config_init(patch):
    patch.object(Config, 'apply')
    Config()
    Config.apply.assert_called_with()


def test_config_apply(init):
    config = Config()
    config.defaults = {'one': 'value'}
    config.apply()
    assert config.one == 'value'


def test_config_apply_from_env(patch, init):
    patch.object(os, 'getenv', return_value='envvalue')
    config = Config()
    config.defaults = {'one': 'value'}
    config.apply()
    assert config.one == 'envvalue'


def test_config_attribute_empty(config):
    assert config.option is None
