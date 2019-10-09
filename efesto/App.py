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
from peewee import IntegrityError

from .Api import Api
from .Blueprints import Blueprints
from .Config import Config
from .Generator import Generator
from .models import Base, Fields, Types, Users, db


class App:

    __slots__ = ()

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
        Base.init_db(config.DB_URL, config.DB_CONNECTIONS,
                     config.DB_TIMEOUT)
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
