# -*- coding: utf-8 -*-
from efesto.models import Base, Users

from peewee import BooleanField, CharField

from pytest import fixture


@fixture
def users(patch):
    patch.object(Users, 'get')


def test_users():
    assert isinstance(Users.identifier, CharField)
    assert Users.identifier.unique
    assert isinstance(Users.superuser, BooleanField)
    assert Users.superuser.default is False
    assert issubclass(Users, Base)


def test_login(magic, users):
    user = magic(identifier='test')
    Users.get.return_value = user
    assert Users.login('test') == user


def test_login_not_found(users):
    def not_found(*args):
        raise Users.DoesNotExist('')
    Users.get.side_effect = not_found
    assert Users.login('test') is None


def test_do_read(magic):
    user = Users()
    query = magic()
    model = magic(others_permission=1, owner_permission=1, group_permission=1)
    user.do('read', query, model)
    query.where.assert_called_with(True)


def test_do_edit(magic):
    user = Users()
    query = magic()
    model = magic(others_permission=2, owner_permission=2, group_permission=2)
    user.do('edit', query, model)
    query.where.assert_called_with(True)


def test_do_eliminate(magic):
    user = Users()
    query = magic()
    model = magic(others_permission=3, owner_permission=3, group_permission=3)
    user.do('eliminate', query, model)
    query.where.assert_called_with(True)


def test_do_user(magic):
    """
    Ensures that permissions work for Users queries
    """
    user = Users()
    query = magic()
    user.do('read', query, Users)
    query.where.assert_called_with(True)
