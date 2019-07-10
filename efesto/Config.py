# -*- coding: utf-8 -*-
from bassoon import Bassoon


class Config(Bassoon):

    defaults = {
        'ADMIN_ENDPOINTS': '0',
        'APP_NAME': 'efesto',
        'BATCH_ENDPOINTS': '1',
        'DB_URL': 'sqlite:///efesto.db',
        'HATEOAS_ENCODER': 'siren',
        'JWT_SECRET': 'secret',
        'JWT_LEEWAY': '5',
        'JWT_AUDIENCE': 'efesto',
        'LOG_LEVEL': 'info',
        'LOG_FORMAT': '[{time:YYYY-MM-DD HH:mm:ss}] [{level}] {message}',
        'PUBLIC_ENDPOINTS': 'index,version',
        'SWAGGER': '1',
        'XCLACKS': '1'
    }
