# -*- coding: utf-8 -*-
from ..Version import version


class Version:

    @staticmethod
    def on_get(request, response):
        data = {
            'properties': {'version': version},
            'links': [{'href': '/version', 'rel': 'self'}],
            'class': ['Version']
        }
        response.body = data
