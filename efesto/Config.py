# -*- coding: utf-8 -*-
from bassoon import Bassoon


class Config(Bassoon):

    defaults = {
        'db_url': 'sqlite:///efesto.db',
        'jwt_secret': 'secret',
        'jwt_leeway': 5,
        'jwt_audience': 'efesto'
    }
