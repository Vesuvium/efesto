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
from efesto.middlewares import Db

from pytest import fixture


@fixture
def db(magic):
    return Db('config', 'db')


def test_db_process_request(magic, db):
    db.db = magic()
    db.process_request('request', 'response')
    assert db.db.connect.call_count == 1


def test_db_process_response(magic, db):
    db.db = magic()
    db.process_response('request', 'response', 'resposnse', 'yes')
    assert db.db.close.call_count == 1
