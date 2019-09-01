# -*- coding: utf-8 -*-
import sys

from efesto.middlewares import Log

from loguru import logger

from pytest import fixture


@fixture
def log(patch, config):
    patch.many(logger, ['remove', 'add'])
    return Log(config)


def test_log_init(log, config):
    assert log.level == config.LOG_LEVEL.upper()
    assert log.format == config.LOG_FORMAT
    assert logger.remove.call_count == 1
    logger.add.assert_called_with(sys.stdout, format=log.format,
                                  level=log.level)


def test_log_process_response(patch, log, http_request, response):
    patch.object(logger, 'info')
    response.status = 'code name'
    http_request.method = 'method'
    http_request.url = 'url'
    log.process_response(http_request, response, 'resource', 'success')
    logger.info.assert_called_with('[code] [method] url')
