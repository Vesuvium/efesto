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

    @staticmethod
    def collection(model):
        return Collections(model)

    @staticmethod
    def item(model):
        return Items(model)

    def list_route(self, endpoint, model):
        self.api.add_route(endpoint, self.collection(model))

    def object_route(self, endpoint, model):
        route = '{}/{}'.format(endpoint, '{id}')
        self.api.add_route(route, self.item(model))

    def add_endpoint(self, endpoint, model):
        self.list_route(endpoint, model)
        self.object_route(endpoint, model)

    def dynamic_endpoints(self, types):
        generator = Generator()
        for dynamic_type in types:
            model = generator.generate(dynamic_type)
            self.add_endpoint('/{}'.format(dynamic_type.name), model)

    def start(self):
        """
        Mounts the routes and starts the API
        """
        for type in Types.select().execute():
            self.type_route(type)
        for route, handler in self.routes.items():
            self.add_endpoint(route, handler)
        return self.api

    def cherries(self):
        """
        This method is the cherry on the cake
        """
        return self.api
