# -*- coding: utf-8 -*-
from bassoon import Bassoon


class Config(Bassoon):

    defaults = {
        'DB_URL': 'sqlite:///efesto.db',
        'HATEOAS_ENCODER': 'siren',
        'JWT_SECRET': 'secret',
        'JWT_LEEWAY': '5',
        'JWT_AUDIENCE': 'efesto',
        'LOG_LEVEL': 'error',
        'APP_NAME': 'efesto',
        'ADMIN_ENDPOINTS': '0'
    }
