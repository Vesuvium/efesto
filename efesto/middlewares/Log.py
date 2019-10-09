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

from loguru import logger


class Log:

    __slots__ = ('level', 'format')

    def __init__(self, config):
        self.level = config.LOG_LEVEL.upper()
        self.format = config.LOG_FORMAT
        logger.remove()
        logger.add(sys.stdout, format=self.format, level=self.level)

    def process_response(self, request, response, resource, success):
        status = response.status.split()[0]
        logger.info(f'[{status}] [{request.method}] {request.url}')
