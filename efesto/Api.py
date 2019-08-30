# -*- coding: utf-8 -*-
import falcon

from .Generator import Generator
from .Routes import Routes
from .handlers import Collections, Items, Version
from .middlewares import Authentication, Json, Log
from .models import Fields, Types, Users


class Api:

    routes = {
        '/fields': {'model': Fields, 'handler': Collections},
        '/fields/{id}': {'model': Fields, 'handler': Items},
        '/types': {'model': Types, 'handler': Collections},
        '/types/{id}': {'model': Types, 'handler': Items},
        '/users': {'model': Users, 'handler': Collections},
        '/users/{id}': {'model': Users, 'handler': Items},
        '/version': Version
    }

    def __init__(self, config):
        self.config = config
        self.generator = Generator()
        self.api = None

    def type_route(self, type):
        """
        Adds a type route from a Type found in the database.
        """
        model = self.generator.generate(type)
        endpoint = f'/{type.name}'
        items_endpoint = f'{endpoint}/{{id}}'
        self.add_routes((
            (endpoint, Collections, model), (items_endpoint, Items, model)
        ))

    def add_route(self, endpoint, handler, model=None):
        if model:
            return self.api.add_route(endpoint, handler(model))
        return self.api.add_route(endpoint, handler)

    def add_routes(self, routes):
        for route in routes:
            self.add_route(*route)

    def middlewares(self):
        return [
            Authentication(self.config.JWT_SECRET, self.config.JWT_AUDIENCE,
                           self.config.PUBLIC_ENDPOINTS),
            Json(),
            Log(self.config.LOG_LEVEL, self.config.LOG_FORMAT)
        ]

    def start(self):
        """
        Mounts the routes and starts the API
        """
        self.api = falcon.API(middleware=self.middlewares())
        for type in Types.select().execute():
            self.type_route(type)
        self.add_routes(Routes.routes)
        return self.api
