# -*- coding: utf-8 -*-
from efesto.Generator import Generator
from efesto.handlers import Collections, Items

import falcon


class Api:

    def __init__(self, **kwargs):
        self.api = falcon.API(**kwargs)

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

    def cherries(self):
        """
        This method is the cherry on the cake
        """
        return self.api
