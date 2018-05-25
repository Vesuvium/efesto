# -*- coding: utf-8 -*-
import os

from efesto.models import Fields, Types

from ruamel.yaml import YAML


class Blueprints:

    def __init__(self):
        self.yaml = YAML(typ='safe')

    @staticmethod
    def make_field(field_name, type_id, **options):
        field = Fields.create(name=field_name, type_id=type_id, owner_id=1,
                              **options)
        field.save()

    @staticmethod
    def options(options):
        dictionary = {}
        for option in options:
            option_name = list(option.keys())[0]
            dictionary[option_name] = option[option_name]
        return dictionary

    def load_field(self, new_type, field):
        """
        Loads a field in the database. If a field section is specified, parse
        it.
        """
        if isinstance(field, str):
            return self.make_field(field, new_type.id)
        for field_name, options in field.items():
            options_dict = self.options(options)
            return self.make_field(field_name, new_type.id, **options_dict)

    @staticmethod
    def load_type(table):
        """
        Loads a type in the database
        """
        return Types.create(name=table, owner_id=1)

    def read(self, blueprint):
        """
        Finds and reads blueprint
        """
        path = os.path.join(os.getcwd(), blueprint)
        if os.path.isfile(path) is False:
            raise ValueError
        with open(path) as f:
            return self.yaml.load(f)

    def parse(self, yaml):
        """
        Parses the content of a blueprint
        """
        for table in yaml:
            new_type = self.load_type(table)
            for field in yaml[table]:
                self.load_field(new_type, field)

    def load(self, filename):
        """
        Load a blueprint in the database
        """
        self.parse(self.read(filename))
