# -*- coding: utf-8 -*-
from ..models import db


class Db:

    __slots__ = ()

    def __init__(self, config):
        pass

    def process_request(self, request, response):
        db.connect(reuse_if_open=True)

    def process_response(self, request, response, resource, success):
        db.close()
