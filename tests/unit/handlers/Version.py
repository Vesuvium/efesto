# -*- coding: utf-8 -*-
import json

from efesto.Version import version
from efesto.handlers import Version


def test_version_on_get(patch, response):
    patch.object(json, 'dumps')
    Version.on_get('request', response)
    json.dumps.assert_called_with({'version': version})
    assert response.body == json.dumps()
