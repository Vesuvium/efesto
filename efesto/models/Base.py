# -*- coding: utf-8 -*-
from peewee import IntegerField, Model, PostgresqlDatabase, SQL, SqliteDatabase

from playhouse import db_url

from .Database import db


class Base(Model):

    conversions = {
        'AutoField': 'number',
        'BigIntegerField': 'number',
        'BooleanField': 'number',
        'CharField': 'text',
        'DateField': 'date',
        'DateTimeField': 'datetime',
        'DecimalField': 'number',
        'DoubleField': 'number',
        'FloatField': 'number',
        'ForeignKeyField': 'number',
        'IntegerField': 'number',
        'TextField': 'text',
        'UUIDField': 'text'
    }

    class Meta:
        database = db

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
    def db_instance(url, **kwargs):
        """
        Create the correct database instance from the url
        """
        dictionary = db_url.parse(url)
        name = dictionary.pop('database')
        if url.startswith('postgres'):
            return PostgresqlDatabase(name, **dictionary)
        return SqliteDatabase(name, **kwargs)

    @classmethod
    def init_db(cls, url, **kwargs):
        """
        Initailize the database with the instance
        """
        db.initialize(cls.db_instance(url, **kwargs))

    def update_item(self, data):
        for key, value in data.items():
            setattr(self, key, value)
        self.save()

    @classmethod
    def filter(cls, key, value, operator):
        """
        Adds a filter to the current query
        """
        column = getattr(cls, key)
        if isinstance(value, list):
            return cls.q.where(column.in_(value))
        if operator == '!':
            return cls.q.where(column != value)
        elif operator == '>':
            return cls.q.where(column > value)
        elif operator == '<':
            return cls.q.where(column < value)
        elif operator == '~':
            return cls.q.where(column.startswith(value))
        return cls.q.where(column == value)

    @staticmethod
    def cast(value):
        if value == 'true':
            return True
        elif value == 'false':
            return False
        elif value == 'null':
            return None
        return value

    @classmethod
    def query(cls, key, value):
        """
        Builds a select query
        """
        if hasattr(cls, key) is False:
            return None
        operator = None
        if value[0] in ['!', '>', '<', '~']:
            operator = value[0]
            value = value[1:]
        cls.q = cls.filter(key, cls.cast(value), operator)

    group = IntegerField(default=1, constraints=[SQL('DEFAULT 1')])
    owner_permission = IntegerField(default=3, constraints=[SQL('DEFAULT 3')])
    group_permission = IntegerField(default=0, constraints=[SQL('DEFAULT 0')])
    others_permission = IntegerField(default=0, constraints=[SQL('DEFAULT 0')])
