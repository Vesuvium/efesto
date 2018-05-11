# -*- coding: utf-8 -*-
from peewee import IntegerField, Model, SQL

from playhouse import db_url

from .Database import db


class Base(Model):

    conversions = {
        'AutoField': 'number',
        'BooleanField': 'number',
        'CharField': 'text',
        'DateTimeField': 'date',
        'FloatField': 'number',
        'ForeignKeyField': 'number',
        'IntegerField': 'number',
        'PrimaryKeyField': 'number'
    }

    class Meta:
        database = db
        validate_backrefs = False

    @classmethod
    def get_columns(cls):
        """
        Produces a list of columns for the current model.
        """
        columns = []
        for name, column in cls._meta.fields.items():
            column_type = cls.conversions[column.__class__.__name__]
            columns.append({'name': name, 'type': column_type})
        return columns

    @staticmethod
    def init_db(url):
        dictionary = db_url.parse(url)
        name = dictionary.pop('database')
        db.init(name, **dictionary)

    def update_item(self, data):
        for key, value in data.items():
            setattr(self, key, value)
        self.save()

    @classmethod
    def filter(cls, key, value, operator):
        """
        Adds a filter to the current query
        """
        if operator == '!':
            return cls.q.where(getattr(cls, key) != value)
        elif operator == '>':
            return cls.q.where(getattr(cls, key) > value)
        elif operator == '<':
            return cls.q.where(getattr(cls, key) < value)
        return cls.q.where(getattr(cls, key) == value)

    @classmethod
    def query(cls, key, value):
        """
        Builds a select query
        """
        if hasattr(cls, key) is False:
            return None
        operator = None
        if value[0] in ['!', '>', '<']:
            operator = value[0]
            value = value[1:]
        cls.q = cls.filter(key, value, operator)

    group = IntegerField(default=1, constraints=[SQL('DEFAULT 1')])
    owner_permission = IntegerField(default=3, constraints=[SQL('DEFAULT 3')])
    group_permission = IntegerField(default=1, constraints=[SQL('DEFAULT 1')])
    others_permission = IntegerField(default=0, constraints=[SQL('DEFAULT 0')])
