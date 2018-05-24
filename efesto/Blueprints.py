# -*- coding: utf-8 -*-
import os

from efesto.models import Fields, Types

from ruamel.yaml import YAML


class Blueprints:

    def __init__(self):
        self.yaml = YAML()

    def field_type(self, field_section, field):
        field.field_type = self.parser.get(field_section, 'type')

    def field_unique(self, field_section, field):
        field.unique = self.parser.getboolean(field_section, 'unique',
                                              fallback=False)

    def field_nullable(self, field_section, field):
        field.nullable = self.parser.getboolean(field_section, 'nullable',
                                                fallback=False)

    def load_field(self, section, field, new_type):
        """
        Loads a field in the database. If a field section is specified, parse
        it.
        """
        new_field = Fields.create(name=field, type_id=new_type.id, owner_id=1)
        field_section = '{}.{}'.format(section, field)
        if self.parser.has_section(field_section):
            self.field_type(field_section, new_field)
            self.field_unique(field_section, new_field)
            self.field_nullable(field_section, new_field)
        new_field.save()

    def section_fields(self, section):
        """
        Finds the fields for a section
        """
        if self.parser.has_option(section, 'fields'):
            return self.parser.get(section, 'fields')

    @staticmethod
    def load_type(section):
        """
        Loads a type in the database
        """
        return Types.create(name=section, owner_id=1)

    def read(self, blueprint):
        """
        Finds and reads blueprint
        """
        path = os.path.join(os.getcwd(), blueprint)
        if os.path.isfile(path) is False:
            raise ValueError
        with open(path) as f:
            return self.yaml.load(f)

    def parse(self):
        """
        Parses the content of a blueprint
        """
        for section in self.parser.sections():
            if '.' not in section:
                new_type = self.load_type(section)
                fields = self.section_fields(section)
                for field in fields.split(','):
                    self.load_field(section, field.strip(), new_type)

    def load(self, filename):
        """
        Load a blueprint in the database
        """
        self.parse(self.read(filename))
