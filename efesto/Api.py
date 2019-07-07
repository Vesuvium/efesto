# -*- coding: utf-8 -*-
import falcon

from .Generator import Generator
from .handlers import Collections, Items
from .models import Fields, Types, Users


class Api:

    routes = {
        '/fields': {'model': Fields, 'handler': Collections},
        '/fields/{id}': {'model': Fields, 'handler': Items},
        '/types': {'model': Types, 'handler': Collections},
        '/types/{id}': {'model': Types, 'handler': Items},
        '/users': {'model': Users, 'handler': Collections},
        '/users/{id}': {'model': Users, 'handler': Items}
    }

    def __init__(self, **kwargs):
        self.api = falcon.API(**kwargs)
        self.generator = Generator()


    def add_endpoint(self, route, handler):
        self.api.add_route(route, handler['handler'](handler['model']))

    def start(self):
        """
        Mounts the routes and starts the API
        """
        for type in Types.select().execute():
            self.type_route(type)
        for route, handler in self.routes.items():
            self.add_endpoint(route, handler)
        return self.api
