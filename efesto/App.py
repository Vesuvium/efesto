# -*- coding: utf-8 -*-
from .Api import Api
from .Config import Config
from .Middlewares import Authentication
from .models import Base, Fields, Types, Users


class App:

    def run():
        """
        Runs efesto
        """
        config = Config()
        Base.init_db(config.db_url)
        middleware = Authentication(config.jwt_secret, config.jwt_audience)
        api = Api(middleware=middleware)
        api.add_endpoint('/users', Users)
        api.add_endpoint('/fields', Fields)
        api.add_endpoint('/types', Types)
        types = Types.select().execute()
        api.dynamic_endpoints(types)
        return api.cherries()
