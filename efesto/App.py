# -*- coding: utf-8 -*-
from .Api import Api
from .Config import Config
from .middlewares import Authentication
from .models import Base, Fields, Types, Users, db


class App:

    @staticmethod
    def config():
        return Config()

    @classmethod
    def run(cls):
        """
        Runs efesto
        """
        config = cls.config()
        Base.init_db(config.DB_URL)
        middleware = Authentication(config.JWT_SECRET, config.JWT_AUDIENCE)
        return Api(middleware=middleware).start()

    @classmethod
    def install(cls):
        """
        Installs efesto by creating the base tables.
        """
        config = cls.config()
        Base.init_db(config.DB_URL)
        db.create_tables([Fields, Types, Users])
