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
