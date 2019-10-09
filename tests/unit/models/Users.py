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
from efesto.models import Base, Users

from peewee import BooleanField, CharField

from pytest import fixture


@fixture
def user():
    return Users()


def test_users():
    assert isinstance(Users.identifier, CharField)
    assert Users.identifier.unique
    assert isinstance(Users.superuser, BooleanField)
    assert Users.superuser.default is False
    assert issubclass(Users, Base)


def test_users_login(patch, magic):
    patch.object(Users, 'get')
    user = magic(identifier='test')
    Users.get.return_value = user
    assert Users.login('test') == user


def test_users_login_not_found(patch, user):
    patch.object(Users, 'get')

    def not_found(*args):
        raise Users.DoesNotExist('')
    Users.get.side_effect = not_found
    assert Users.login('test') is None


def test_users_do_read(magic, user):
    query = magic()
    model = magic(others_permission=1, owner_permission=1, group_permission=1)
    user.do('read', query, model)
    query.where.assert_called_with(True)


def test_users_do_edit(magic, user):
    query = magic()
    model = magic(others_permission=2, owner_permission=2, group_permission=2)
    user.do('edit', query, model)
    query.where.assert_called_with(True)


def test_users_do_eliminate(magic, user):
    query = magic()
    model = magic(others_permission=3, owner_permission=3, group_permission=3)
    user.do('eliminate', query, model)
    query.where.assert_called_with(True)


def test_users_do_user(magic, user):
    """
    Ensures that permissions work for Users queries
    """
    query = magic()
    user.do('read', query, Users)
    query.where.assert_called_with(True)


def test_users_do_superuser(magic, user):
    """
    Ensures superuser permissions are applied correctly
    """
    user.superuser = True
    model = magic(others_permission=0, owner_permission=0, group_permission=0)
    query = magic()
    assert user.do('read', query, model) == query
