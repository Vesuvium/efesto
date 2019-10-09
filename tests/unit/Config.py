#   Copyright (C) 2018  Jacopo Cascioli
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
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
    assert Config.defaults['DB_CONNECTIONS'] == '32'
    assert Config.defaults['DB_TIMEOUT'] == '300'
    assert Config.defaults['DB_URL'] == db_url
    assert Config.defaults['HATEOAS_ENCODER'] == 'siren'
    assert Config.defaults['JWT_SECRET'] == 'secret'
    assert Config.defaults['JWT_LEEWAY'] == '5'
    assert Config.defaults['JWT_AUDIENCE'] == 'efesto'
    assert Config.defaults['LOG_LEVEL'] == 'info'
    format = '[{time:YYYY-MM-DD HH:mm:ss}] [{level}] {message}'
    assert Config.defaults['LOG_FORMAT'] == format
    assert Config.defaults['MIDDLEWARES'] == 'db:authentication:json:log'
    assert Config.defaults['PUBLIC_ENDPOINTS'] == 'index,version'
    assert Config.defaults['SWAGGER'] == '1'
