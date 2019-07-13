# -*- coding: utf-8 -*-
from efesto.Version import version
from efesto.handlers import Version


def test_version_on_get(response):
    Version.on_get('request', response)
    data = {'properties': {'version': version},
            'links': [{'href': '/version', 'rel': 'self'}],
            'class': ['Version']}
    assert response.body == data
