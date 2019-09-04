# -*- coding: utf-8 -*-
import falcon

from .Generator import Generator
from .Routes import Routes
from .handlers import Collections, Items
from .middlewares import Authentication, Clacks, Db, Json, Log, Msgpack
from .models import Types


class Api:

    __slots__ = ('config', 'generator', 'api')

    available_middlewares = {
        'authentication': Authentication,
        'clacks': Clacks,
        'db': Db,
        'json': Json,
        'log': Log,
        'msgpack': Msgpack
    }

    def __init__(self, config):
        self.config = config
        self.generator = Generator()
        self.api = None

    def route(self, endpoint, handler, model=None):
        if model:
            return self.api.add_route(endpoint, handler(model))
        return self.api.add_route(endpoint, handler)

    def routes(self, routes):
        for route in routes:
            self.route(*route)

    def custom_route(self, name, model):
        endpoint = f'/{name}'
        items_endpoint = f'{endpoint}/{{id}}'
        self.routes((
            (endpoint, Collections, model), (items_endpoint, Items, model)
        ))

    def custom_routes(self, custom_types):
        for custom_type in custom_types:
            model = self.generator.generate(custom_type)
            self.custom_route(custom_type.name, model)

    def middlewares(self):
        middlewares = []
        for name in self.config.MIDDLEWARES.lower().split(':'):
            if name in self.available_middlewares:
                middleware = self.available_middlewares[name]
                middlewares.append(middleware(self.config))
        return middlewares

    def falcon(self):
        return falcon.API(middleware=self.middlewares())

    def start(self):
        """
        Mounts the routes and starts the API
        """
        self.api = self.falcon()
        self.custom_routes(Types.select().execute())
        self.routes(Routes.routes)
        return self.api
