#   Copyright (C) 2018  Jacopo Cascioli
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
# -*- coding: utf-8 -*-
from efesto.Siren import Siren

from pytest import mark


def test_siren_paginate():
    result = Siren.paginate('path', [], 1, 1)
    assert result[0] == {'rel': ['self'], 'href': 'path'}
    assert result[1] == {'href': 'path?page=2', 'rel': ['next']}


def test_siren_paginate_middle():
    result = Siren.paginate('path', [], 2, 1)
    assert result[0] == {'href': 'path', 'rel': ['self']}
    assert result[1] == {'href': 'path?page=3', 'rel': ['next']}
    assert result[2] == {'href': 'path?page=1', 'rel': ['previous']}


def test_siren_paginate_last():
    result = Siren.paginate('path', [], 3, 0)
    assert result[0] == {'rel': ['self'], 'href': 'path'}
    assert result[1] == {'rel': ['previous'], 'href': 'path?page=2'}


def test_siren_entity():
    item = {'id': 1}
    result = Siren.entity(item, 'type', 'path', [])
    assert result['properties'] == item
    assert result['class'] == ['type']
    assert result['links'] == [{'href': 'path/1', 'rel': 'self'}]


def test_siren_entity__nested():
    item = {'id': 1, 'nested': [{'id': 2}]}
    result = Siren.entity(item, 'type', 'path', ['nested'])
    expected = [Siren.entity({'id': 2}, 'nested', '/nested')]
    assert result['properties']['nested'] == expected


def test_siren_entity__path():
    item = {'id': 1}
    entity = Siren.entity(item, 'type', '/endpoint/1', [])
    assert entity['links'] == [{'href': '/endpoint/1', 'rel': 'self'}]


@mark.parametrize('value, expected', [
    ('1', 'number'), (1, 'number'),
    ('hello', 'text')
])
def test_siren_field_type(value, expected):
    assert Siren.field_type(value) == expected


def test_siren_fields(patch):
    patch.object(Siren, 'field_type')
    result = Siren.fields([{'id': 1}])
    Siren.field_type.assert_called_with(1)
    assert result == [{'id': Siren.field_type()}]


def test_siren_entities(patch):
    patch.many(Siren, ['entity', 'paginate', 'fields'])
    data = [{'id': 1}]
    result = Siren.entities(data, 'type', 'path', [], 1, 1)
    Siren.entity.assert_called_with({'id': 1}, 'type', 'path', [])
    Siren.fields.assert_called_with(data)
    assert result['entities'] == [Siren.entity()]
    assert result['actions'][0] == {'name': 'add-type', 'method': 'POST',
                                    'type': 'application/json',
                                    'fields': Siren.fields()}
    assert result['links'] == Siren.paginate()


def test_siren_encode(patch):
    patch.object(Siren, 'entity')
    result = Siren.encode('data', [], 'item_type', 'path', 1, 1)
    Siren.entity.assert_called_with('data', 'item_type', 'path', [])
    assert result == Siren.entity()


def test_siren_encode__entities(patch):
    patch.object(Siren, 'entities')
    result = Siren.encode(['data'], [], 'item_type', 'path', 1, 1)
    Siren.entities.assert_called_with(['data'], 'item_type', 'path', [], 1, 1)
    assert result == Siren.entities()
