# -*- coding: utf-8 -*-
from efesto.models import Base, db

from peewee import (AutoField, BigIntegerField, BooleanField, CharField,
                    DateField, DateTimeField, DecimalField, DoubleField,
                    FloatField, ForeignKeyField, IntegerField, IntegrityError,
                    Model, SQL, SqliteDatabase, TextField, UUIDField)

from playhouse import db_url
from playhouse.pool import PooledPostgresqlExtDatabase as PooledPostrgres

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
    assert Base.group_permission.default == 0
    assert Base.group_permission.constraints == [SQL('DEFAULT 0')]
    assert isinstance(Base.others_permission, IntegerField)
    assert Base.others_permission.default == 0
    assert Base.others_permission.constraints == [SQL('DEFAULT 0')]
    assert issubclass(Base, Model)


@mark.parametrize('field, field_type', [
    (AutoField, 'number'),
    (BigIntegerField, 'number'),
    (BooleanField, 'number'),
    (CharField, 'text'),
    (DateField, 'date'),
    (DateTimeField, 'datetime'),
    (DecimalField, 'number'),
    (DoubleField, 'number'),
    (FloatField, 'number'),
    (IntegerField, 'number'),
    (TextField, 'text'),
    (UUIDField, 'text')

])
def test_get_columns(field, field_type):
    Base._meta.fields = {'field': field()}
    columns = Base.get_columns()
    assert columns[0] == {'name': 'field', 'type': field_type}


def test_get_columns_foreign_key():
    Base._meta.fields = {'field': ForeignKeyField(Base)}
    columns = Base.get_columns()
    assert columns[0] == {'name': 'field', 'type': 'number'}


def test_base_db_instance(patch):
    patch.init(SqliteDatabase)
    patch.object(db_url, 'parse')
    result = Base.db_instance('url', 'connections', '300')
    db_url.parse.assert_called_with('url')
    db_url.parse().pop.assert_called_with('database')
    SqliteDatabase.__init__.assert_called_with(db_url.parse().pop())
    assert isinstance(result, SqliteDatabase)


def test_base_db_instance__postgres(patch):
    patch.init(PooledPostrgres)
    patch.object(db_url, 'parse')
    result = Base.db_instance('postgres', '32', '300')
    db_str = db_url.parse()
    PooledPostrgres.__init__.assert_called_with(db_str.pop(),
                                                max_connections='32',
                                                stale_timeout='300', **db_str)
    assert isinstance(result, PooledPostrgres)


def test_base_db_instance__extra_options(patch):
    patch.init(SqliteDatabase)
    patch.object(db_url, 'parse')
    Base.db_instance('url', '32', '300', autocommit=False)
    pop = db_url.parse().pop()
    SqliteDatabase.__init__.assert_called_with(pop, autocommit=False)


def test_base_init_db(patch):
    patch.object(Base, 'db_instance')
    patch.object(db, 'initialize')
    Base.init_db('url', '32', '300')
    Base.db_instance.assert_called_with('url', '32', '300')
    db.initialize.assert_called_with(Base.db_instance())


def test_base_init_db_extra_options(patch):
    """
    Ensures Base.init_db passes extra options to Base.db_instance
    """
    patch.object(Base, 'db_instance')
    patch.object(db, 'initialize')
    Base.init_db('url', '32', '300', autocommit=False)
    Base.db_instance.assert_called_with('url', '32', '300', autocommit=False)


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


def test_base_filter_list(magic):
    """
    Ensures a list produces an IN query.
    """
    Base.q = magic()
    Base.key = magic()
    Base.model = magic(key='value')
    Base.filter('key', ['a', 'b'], None)
    Base.key.in_.assert_called_with(['a', 'b'])
    Base.q.where.assert_called_with(Base.key.in_())


def test_base_filter_operators_startswith(magic):
    """
    Ensures ~ produces a startswith query.
    """
    Base.q = magic()
    Base.key = magic()
    Base.model = magic(key='value')
    Base.filter('key', 'value', '~')
    Base.key.startswith.assert_called_with('value')
    Base.q.where.assert_called_with(Base.key.startswith())


def test_base_cast():
    assert Base.cast('true') is True


def test_base_cast_false():
    assert Base.cast('false') is False


def test_base_cast_none():
    assert Base.cast('null') is None


def test_base_query(patch, magic):
    patch.many(Base, ['filter', 'cast'])
    Base.query('key', 'value')
    Base.cast.assert_called_with('value')
    Base.filter.assert_called_with('key', Base.cast(), None)
    assert Base.q == Base.filter()


def test_base_query_not_field(patch, magic):
    Base.q = None
    patch.many(Base, ['filter', 'cast'])
    Base.query('nokey', 'value')
    assert Base.q is None


@mark.parametrize('operator', ['!', '>', '<', '~'])
def test_base_query_operators(patch, magic, operator):
    patch.many(Base, ['filter', 'cast'])
    Base.query('key', '{}value'.format(operator))
    Base.cast.assert_called_with('value')
    Base.filter.assert_called_with('key', Base.cast(), operator)


@mark.skip
def test_base_write(patch, magic):
    patch.object(db, 'atomic')
    patch.object(Base, 'create')
    result = Base.write(args='args')
    Base.create.assert_called_with(args='args')
    assert result == Base.create()


@mark.skip
@mark.parametrize('error', [IntegrityError, ValueError])
def test_base_write_error(patch, magic, error):
    patch.object(db, 'atomic')
    patch.object(Base, 'create', side_effect=error)
    assert Base.write(args='args') is None


def test_base_update_item(patch, base):
    patch.object(Base, 'save')
    result = base.update_item({'hello': 'world'})
    assert base.hello == 'world'
    assert result == base.save()


@mark.skip
def test_base_edit(patch, base):
    patch.object(db, 'atomic')
    patch.object(Base, 'update_item')
    result = base.edit({'hello': 'world'})
    Base.update_item.assert_called_with({'hello': 'world'})
    assert result == Base.update_item()


@mark.skip
def test_base_edit_error(patch, magic):
    patch.object(db, 'atomic')
    patch.object(Base, 'update_item', side_effect=IntegrityError)
    assert Base.edit({'hello': 'world'}) is None
