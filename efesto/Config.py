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


class Config(Bassoon):

    defaults = {
        'ADMIN_ENDPOINTS': '0',
        'APP_NAME': 'efesto',
        'BATCH_ENDPOINTS': '1',
        'DB_CONNECTIONS': '32',
        'DB_TIMEOUT': '300',
        'DB_URL': 'sqlite:///efesto.db',
        'HATEOAS_ENCODER': 'siren',
        'JWT_SECRET': 'secret',
        'JWT_LEEWAY': '5',
        'JWT_AUDIENCE': 'efesto',
        'LOG_LEVEL': 'info',
        'LOG_FORMAT': '[{time:YYYY-MM-DD HH:mm:ss}] [{level}] {message}',
        'MIDDLEWARES': 'db:authentication:json:log',
        'PUBLIC_ENDPOINTS': 'index,version',
        'SWAGGER': '1'
    }
