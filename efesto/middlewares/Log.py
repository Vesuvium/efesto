# -*- coding: utf-8 -*-
import sys

from loguru import logger


class Log:

    def __init__(self):
        logger.remove()
        format = '[{time:YYYY-MM-DD HH:mm:ss}] [{level}] {message}'
        logger.add(sys.stdout, format=format)

    def process_response(self, request, response, resource, success):
        status = response.status.split()[0]
        logger.info(f'[{status}] [{request.method}] {request.url}')
