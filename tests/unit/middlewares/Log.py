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
import sys

from efesto.middlewares import Log

from loguru import logger

from pytest import fixture


@fixture
def log(patch, config):
    patch.many(logger, ['remove', 'add'])
    return Log(config, 'db')


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
