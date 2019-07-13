# -*- coding: utf-8 -*-
import falcon

from .Generator import Generator
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
        self.routes[endpoint] = {'model': model, 'handler': Collections}
        self.routes[f'{endpoint}/{{id}}'] = {'model': model, 'handler': Items}

    def add_endpoint(self, route, handler):
        if type(handler) == dict:
            self.api.add_route(route, handler['handler'](handler['model']))
        else:
            self.api.add_route(route, handler)

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
        for route, handler in self.routes.items():
            self.add_endpoint(route, handler)
        return self.api
