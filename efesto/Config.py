# -*- coding: utf-8 -*-
from bassoon import Bassoon


class Config(Bassoon):

    defaults = {
        'DB_URL': 'sqlite:///efesto.db',
        'JWT_SECRET': 'secret',
        'JWT_LEEWAY': '5',
        'JWT_AUDIENCE': 'efesto',
        'APP_NAME': 'efesto',
        'ADMIN_ENDPOINTS': '0'
    }
