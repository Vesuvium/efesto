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
from efesto.models import Base


from psyker import Column, Psyker


def test_base_permissions(patch):
    patch.init(Column)
    result = Base.permissions()
    assert isinstance(result['group'], Column)
    assert isinstance(result['owner_permission'], Column)
    assert isinstance(result['group_permission'], Column)
    assert isinstance(result['others_permission'], Column)


def test_base_init_db(patch):
    patch.init(Psyker)
    patch.many(Psyker, ['add_models', 'start'])
    result = Base.init_db('url', ['models'], 'connections', 'timeout')
    Psyker.add_models.assert_called_with('models')
    Psyker.start.assert_called_with('url')
    assert isinstance(result, Psyker)


def test_base_filter(magic):
    Base.q = magic()
    result = Base.filter('key', 'value', 'operator')
    Base.q.where.assert_called_with(key=('operator', 'value'))
    assert result == Base.q.where()


def test_base_cast():
    assert Base.cast('true') is True


def test_base_cast_false():
    assert Base.cast('false') is False


def test_base_cast_none():
    assert Base.cast('null') is None


def test_base_write(patch):
    patch.init(Base)
    patch.object(Base, 'save')
    result = Base.write(col='value')
    Base.__init__.assert_called_with(col='value')
    assert result == Base.save()


def test_base_edit(patch):
    patch.object(Base, 'update')
    result = Base.edit('id', col='value')
    Base.update.assert_called_with(col='value')
    Base.update().where.assert_called_with(id='id')
    assert result == Base.update().where().execute()
