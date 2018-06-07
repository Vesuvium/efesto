# -*- coding: utf-8 -*
from efesto.Siren import Siren

from pytest import fixture


@fixture
def siren(patch):
    patch.init(Siren)
    patch.object(Siren, 'encode')
    return Siren
