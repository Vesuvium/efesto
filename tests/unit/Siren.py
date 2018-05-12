# -*- coding: utf-8 -*-
from efesto.Siren import Siren

from pytest import fixture

import ujson


@fixture
def siren():
    return Siren()


def test_siren_paginate():
    links = Siren().paginate('path', [], 1, 1)
    assert links[0] == {'rel': ['self'], 'href': 'path'}
    assert links[1] == {'href': 'path?page=2', 'rel': ['next']}


def test_siren_paginate_middle():
    links = Siren().paginate('path', [], 2, 1)
    assert links[0] == {'href': 'path', 'rel': ['self']}
    assert links[1] == {'href': 'path?page=3', 'rel': ['next']}
    assert links[2] == {'href': 'path?page=1', 'rel': ['previous']}


def test_siren_paginate_last():
    links = Siren().paginate('path', [], 3, 0)
    assert links[0] == {'rel': ['self'], 'href': 'path'}
    assert links[1] == {'rel': ['previous'], 'href': 'path?page=2'}


def test_siren_entity(magic, siren):
    item = magic(__data__='data')
    entity = siren.entity('', item)
    assert entity['properties'] == item.__data__
    assert entity['class'] == [item.__class__.__name__]
    assert entity['links'] == [{'href': '/{}'.format(item.id), 'rel': 'self'}]


def test_siren_entity_path(magic, siren):
    item = magic(id=1, __data__='data')
    entity = siren.entity('/endpoint/1', item)
    assert entity['links'] == [{'href': '/endpoint/1', 'rel': 'self'}]


def test_siren_make_entities(patch, magic, siren):
    patch.many(Siren, ['entity', 'paginate'])
    item = magic()
    siren.data = [item]
    entities = siren.make_entities()
    Siren.entity.assert_called_with(siren.path, item)
    assert entities['entities'] == [Siren.entity()]
    assert type(entities['actions']) == list
    assert entities['links'] == Siren.paginate()


def test_siren_encode(patch):
    patch.object(Siren, 'make_entities')
    patch.object(ujson, 'dumps')
    Siren().encode('utf-8')
    ujson.dumps.assert_called_with(Siren.make_entities())


def test_siren_encode_one(patch, siren):
    patch.object(Siren, 'entity')
    patch.object(ujson, 'dumps')
    siren.data = {}
    siren.encode('utf-8')
    Siren.entity.assert_called_with(siren.path, siren.data)
    ujson.dumps.assert_called_with(Siren.entity())
