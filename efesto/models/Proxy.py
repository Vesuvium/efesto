# -*- coding: utf-8 -*-


class Proxy(object):
    """
    Create a proxy or placeholder for another object.
    This is an alternative version of the original, that instead
    used slot and was untestable.
    """

    def __init__(self):
        self._callbacks = []
        self.initialize(None)

    def initialize(self, obj):
        self.obj = obj
        for callback in self._callbacks:
            callback(obj)

    def attach_callback(self, callback):
        self._callbacks.append(callback)
        return callback

    def passthrough(method):
        def inner(self, *args, **kwargs):
            if self.obj is None:
                raise AttributeError('Cannot use uninitialized Proxy.')
            return getattr(self.obj, method)(*args, **kwargs)
        return inner

    # Allow proxy to be used as a context-manager.
    __enter__ = passthrough('__enter__')
    __exit__ = passthrough('__exit__')

    def __getattr__(self, attr):
        if self.obj is None:
            raise AttributeError('Cannot use uninitialized Proxy.')
        return getattr(self.obj, attr)
