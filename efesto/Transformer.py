# -*- coding: utf-8 -*-
import os

from ruamel.yaml import YAML


from peewee import (BooleanField, CharField, DateTimeField, FloatField,
                    ForeignKeyField, IntegerField, SQL, TextField)

from .models import Base, Fields, Users


class Transformer:

    mappings = {
        'string': CharField,
        'text': TextField,
        'int': IntegerField,
        'float': FloatField,
        'bool': BooleanField,
        'date': DateTimeField
    }

    def __init__(self):
        self.yaml = YAML(typ='safe')
        self.models = {}

    def read(self, blueprint):
        """
        Finds and reads blueprint
        """
        path = os.path.join(os.getcwd(), blueprint)
        if os.path.isfile(path) is False:
            raise ValueError
        with open(path) as f:
            return self.yaml.load(f)

    def make_field(self, field):
        return CharField()

    def attributes(self, fields):
        attributes = {}
        for field in fields:
            attributes[field] = self.make_field(field)
        return attributes

    def parse(self, yaml):
        """
        Parses the content of a blueprint
        """
        for model in yaml:
            attributes = self.attributes(yaml[model])
            attributes['owner'] = ForeignKeyField(Users)
            self.models[model] = type(model, (Base, ), attributes)

    def transform(self, blueprint):
        self.parse(self.read(blueprint))
