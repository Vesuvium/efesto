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
from .Api import Api
from .Blueprints import Blueprints
from .Config import Config
from .Generator import Generator
from .models import Base, Fields, Types, Users


class App:

    __slots__ = ()

    @staticmethod
    def config():
        return Config()

    @staticmethod
    def generator(db):
        return Generator(db)

    @classmethod
    def db(cls, config):
        return Base.init_db(config.DB_URL, (Users, Types, Fields),
                            config.DB_CONNECTIONS, config.DB_TIMEOUT)

    @classmethod
    def init(cls):
        return cls.db(cls.config())

    @classmethod
    def run(cls):
        """
        Runs efesto
        """
        config = cls.config()
        return Api(config, cls.db(config)).start()

    @classmethod
    def install(cls):
        """
        Installs efesto by creating the base tables.
        """
        cls.init()

    @classmethod
    def create_user(cls, identifier, superuser):
        cls.init()
        return Users(identifier=identifier, owner_permission=1,
                     group=1, group_permission=1, others_permission=1,
                     superuser=superuser).save()

    @classmethod
    def load(cls, filename):
        """
        Loads a blueprint.
        """
        db = cls.init()
        Blueprints().load(filename)
        types = Types.select().get()
        generator = cls.generator(db)
        for dynamic_type in types:
            generator.generate(dynamic_type)
