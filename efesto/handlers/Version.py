# -*- coding: utf-8 -*-
import json

from ..Version import version


class Version:

    @staticmethod
    def on_get(request, response):
        data = {
            'properties': {'version': version},
            'links': [{'href': '/version', 'rel': 'self'}],
            'class': ['Version']
        }
        response.body = json.dumps(data)
