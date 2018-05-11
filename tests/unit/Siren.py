# -*- coding: utf-8 -*-
from efesto.Siren import Siren

import ujson


def test_paginate():
    links = Siren().paginate('path', [], 1, 1)
    assert links[0] == {'rel': ['self'], 'href': 'path'}
    assert links[1] == {'href': 'path?page=2', 'rel': ['next']}


def test_paginate_middle():
    links = Siren().paginate('path', [], 2, 1)
    assert links[0] == {'href': 'path', 'rel': ['self']}
    assert links[1] == {'href': 'path?page=3', 'rel': ['next']}
    assert links[2] == {'href': 'path?page=1', 'rel': ['previous']}


def test_paginate_last():
    links = Siren().paginate('path', [], 3, 0)
    assert links[0] == {'rel': ['self'], 'href': 'path'}
    assert links[1] == {'rel': ['previous'], 'href': 'path?page=2'}


def test_make_entity(magic):
    item = magic(__data__='data')
    entity = Siren().make_entity(item)
    assert entity['properties'] == item.__data__
    assert entity['class'] == [item.__class__.__name__]
    assert entity['links'] == [{'href': '/{}'.format(item.id), 'rel': 'self'}]


def test_make_entity_path_ready(magic):
    item = magic(id=1, __data__='data')
    entity = Siren(path='/endpoint/1').make_entity(item)
    assert entity['links'] == [{'href': '/endpoint/1', 'rel': 'self'}]


def test_make_entities(patch, magic):
    patch.object(Siren, 'make_entity')
    patch.object(Siren, 'paginate')
    item = magic()
    entities = Siren(data=[item]).make_entities()
    assert entities['entities'] == [Siren.make_entity()]
    assert type(entities['actions']) == list
    assert entities['links'] == Siren.paginate()


def test_encode(patch):
    patch.object(Siren, 'make_entities')
    patch.object(ujson, 'dumps')
    Siren().encode('utf-8')
    ujson.dumps.assert_called_with(Siren.make_entities())


def test_encode_one(patch):
    patch.object(Siren, 'make_entity')
    patch.object(ujson, 'dumps')
    Siren(data={}).encode('utf-8')
    ujson.dumps.assert_called_with(Siren.make_entity())
