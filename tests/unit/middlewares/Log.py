# -*- coding: utf-8 -*-
import sys

from efesto.middlewares import Log

from loguru import logger

from pytest import fixture


@fixture
def log(patch):
    patch.many(logger, ['remove', 'add'])
    return Log('level', 'format')


def test_log_init(log):
    assert logger.remove.call_count == 1
    logger.add.assert_called_with(sys.stdout, format='format', level='LEVEL')


def test_log_process_response(patch, log, http_request, response):
    patch.object(logger, 'info')
    response.status = 'code name'
    http_request.method = 'method'
    http_request.url = 'url'
    log.process_response(http_request, response, 'resource', 'success')
    logger.info.assert_called_with('[code] [method] url')
