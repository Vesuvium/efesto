# -*- coding: utf-8 -*-
from .Api import Api
from .Config import Config
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
        return Api(config).start()

    @classmethod
    def install(cls):
        """
        Installs efesto by creating the base tables.
        """
        config = cls.config()
        Base.init_db(config.DB_URL)
        db.create_tables([Fields, Types, Users])
