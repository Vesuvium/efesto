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
from efesto.models import db

from pytest import fixture


@fixture
def db_middleware(magic):
    return Db('config')


def test_db_process_request(magic, db_middleware):
    db.connect = magic()
    db_middleware.process_request('request', 'response')
    db.connect.assert_called_with(reuse_if_open=True)


def test_db_process_response(magic, db_middleware):
    db.close = magic()
    db_middleware.process_response('request', 'response', 'resposnse', 'yes')
    assert db.close.call_count == 1
