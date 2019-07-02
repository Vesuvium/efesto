# -*- coding: utf-8 -*-
import json

from ..Version import version


class Version:

    @staticmethod
    def on_get(request, response):
        response.body = json.dumps({'version': version})
