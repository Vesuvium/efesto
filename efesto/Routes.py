# -*- coding: utf-8 -*-
from .handlers import Collections, Items, Version
from .models import Fields, Types, Users


class Routes:
    __slots__ = ()

    routes = (
        ('/fields', Collections, Fields),
        ('/fields/{id}', Items, Fields),
        ('/types', Collections, Types),
        ('/types/{id}', Items, Types),
        ('/users', Collections, Users),
        ('/users/{id}', Items, Users),
        ('/version', Version)
    )
