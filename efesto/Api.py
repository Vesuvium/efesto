# -*- coding: utf-8 -*-
import falcon

from .Generator import Generator
from .Routes import Routes
from .handlers import Collections, Items
from .middlewares import Authentication, Json, Log
from .models import Types


class Api:

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
        return [
            Authentication(self.config.JWT_SECRET, self.config.JWT_AUDIENCE,
                           self.config.PUBLIC_ENDPOINTS),
            Json(),
            Log(self.config.LOG_LEVEL, self.config.LOG_FORMAT)
        ]

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
