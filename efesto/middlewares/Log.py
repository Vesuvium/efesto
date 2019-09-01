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
