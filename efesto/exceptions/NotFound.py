# -*- coding: utf-8 -*-
from falcon import HTTPNotFound


class NotFound(HTTPNotFound):

    def __init__(self):
        super().__init__(title='Not found',
                         description='The requested resource was not found')
