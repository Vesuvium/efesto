# -*- coding: utf-8 -*-
import json

from efesto.Version import version
from efesto.handlers import Version


def test_version_on_get(patch, response):
    patch.object(json, 'dumps')
    Version.on_get('request', response)
    data = {'properties': {'version': version},
            'links': [{'href': '/version', 'rel': 'self'}],
            'class': ['Version']}
    json.dumps.assert_called_with(data)
    assert response.body == json.dumps()
