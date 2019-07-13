# -*- coding: utf-8 -*-
from peewee import IntegrityError

from .Api import Api
from .Blueprints import Blueprints
from .Config import Config
from .Generator import Generator
from .models import Base, Fields, Types, Users, db


class App:

    @staticmethod
    def config():
        return Config()

    @staticmethod
    def generator():
        return Generator()

    @classmethod
    def init(cls):
        """
        Inits database and configuration
        """
        config = cls.config()
        Base.init_db(config.DB_URL)
        return config

    @classmethod
    def run(cls):
        """
        Runs efesto
        """
        return Api(cls.init()).start()

    @classmethod
    def install(cls):
        """
        Installs efesto by creating the base tables.
        """
        cls.init()
        db.create_tables([Fields, Types, Users])

    @classmethod
    def create_user(cls, identifier, superuser):
        cls.init()
        try:
            return Users(identifier=identifier, owner_permission=1,
                         group_permission=1, others_permission=1,
                         superuser=superuser).save()
        except IntegrityError:
            return None

    @classmethod
    def load(cls, filename):
        """
        Loads a blueprint.
        """
        cls.init()
        Blueprints().load(filename)
        types = Types.select().execute()
        generator = cls.generator()
        for dynamic_type in types:
            generator.generate(dynamic_type)
        db.create_tables(generator.models.values(), safe=True)
