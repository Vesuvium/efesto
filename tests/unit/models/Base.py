# -*- coding: utf-8 -*-
from collections import OrderedDict

from efesto.models import Base, db

from peewee import (AutoField, BooleanField, CharField, DateTimeField,
                    FloatField, ForeignKeyField, IntegerField, Model,
                    PrimaryKeyField, SQL, TextField)

from playhouse import db_url

from pytest import fixture, mark


@fixture
def base():
    return Base()


def test_base_model():
    assert isinstance(Base.group, IntegerField)
    assert Base.group.default == 1
    assert Base.group.constraints == [SQL('DEFAULT 1')]
    assert isinstance(Base.owner_permission, IntegerField)
    assert Base.owner_permission.default == 3
    assert Base.owner_permission.constraints == [SQL('DEFAULT 3')]
    assert isinstance(Base.group_permission, IntegerField)
    assert Base.group_permission.default == 1
    assert Base.group_permission.constraints == [SQL('DEFAULT 1')]
    assert isinstance(Base.others_permission, IntegerField)
    assert Base.others_permission.default == 0
    assert Base.others_permission.constraints == [SQL('DEFAULT 0')]
    assert issubclass(Base, Model)


def test_get_columns():
    fields = (
        ('autofield', AutoField()),
        ('boolfield', BooleanField()),
        ('charfield', CharField()),
        ('textfield', TextField()),
        ('datetimefield', DateTimeField()),
        ('floatfield', FloatField()),
        ('foreignfield', ForeignKeyField(Base)),
        ('integerfield', IntegerField()),
        ('primarykeyfield', PrimaryKeyField())
    )
    Base._meta.fields = OrderedDict(fields)
    columns = Base.get_columns()
    assert columns[0] == {'name': 'autofield', 'type': 'number'}
    assert columns[1] == {'name': 'boolfield', 'type': 'number'}
    assert columns[2] == {'name': 'charfield', 'type': 'text'}
    assert columns[3] == {'name': 'textfield', 'type': 'text'}
    assert columns[4] == {'name': 'datetimefield', 'type': 'date'}
    assert columns[5] == {'name': 'floatfield', 'type': 'number'}
    assert columns[6] == {'name': 'foreignfield', 'type': 'number'}
    assert columns[7] == {'name': 'integerfield', 'type': 'number'}
    assert columns[8] == {'name': 'primarykeyfield', 'type': 'number'}


def test_base_init_db(patch):
    patch.object(db_url, 'parse')
    patch.object(db, 'init')
    Base.init_db('url')
    db_url.parse.assert_called_with('url')
    db_url.parse().pop.assert_called_with('database')
    db.init.assert_called_with(db_url.parse().pop(), **db_url.parse())


def test_base_update_item(patch, base):
    patch.object(Base, 'save')
    base.update_item({'hello': 'world'})
    assert base.hello == 'world'
    assert base.save.call_count == 1


def test_base_filter(magic):
    Base.q = magic()
    Base.key = 'value'
    result = Base.filter('key', 'value', None)
    Base.q.where.assert_called_with(True)
    assert result == Base.q.where()


@mark.parametrize('operator', ['!', '<', '>'])
def test_base_filter_operators(magic, operator):
    Base.q = magic()
    Base.key = 'value'
    Base.model = magic(key='value')
    Base.filter('key', 'value', operator)
    Base.q.where.assert_called_with(False)


def test_base_query(patch, magic):
    patch.object(Base, 'filter')
    Base.query('key', 'value')
    Base.filter.assert_called_with('key', 'value', None)
    assert Base.q == Base.filter()


def test_base_query_not_field(patch, magic):
    Base.q = None
    patch.object(Base, 'filter')
    Base.query('nokey', 'value')
    assert Base.q is None


@mark.parametrize('operator', ['!', '>', '<'])
def test_base_query_operators(patch, magic, operator):
    patch.object(Base, 'filter')
    Base.query('key', '{}value'.format(operator))
    Base.filter.assert_called_with('key', 'value', operator)
