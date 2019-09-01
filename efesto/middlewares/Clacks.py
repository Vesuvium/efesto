# -*- coding: utf-8 -*-
class Clacks:

    def __init__(self, config):
        pass

    def process_response(self, request, response, resource, success):
        response.set_header('X-Clacks-Overhead', 'GNU Terry Pratchett')
