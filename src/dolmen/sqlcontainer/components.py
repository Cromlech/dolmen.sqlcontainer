# -*- coding: utf-8 -*-

from cromlech.sqlalchemy import get_session
from zope.location import ILocation, Location, LocationProxy, locate
from zope.interface import implementer
from .interfaces import ISQLContainer


@implementer(ISQLContainer)
class SQLContainer(Location):

    model = None

    def __init__(self, parent, name, db_key):
        self.__parent__ = parent
        self.__name__ = name
        self.db_key = db_key

    def key_reverse(self, obj):
        return obj.id

    def key_converter(self, id):
        return id

    @property
    def session(self):
        return get_session(self.db_key)

    def __getitem__(self, id):
        key = self.key_converter(id)
        model = self.query_filters(self.session.query(self.model)).get(key)
        if model is None:
            raise KeyError(key)

        proxy = ILocation(model, None)
        if proxy is None:
            proxy = LocationProxy(model)
        locate(proxy, self, str(id))
        return proxy

    def query_filters(self, query):
        return query

    def __iter__(self):
        models = self.query_filters(self.session.query(self.model))
        for model in models:
            proxy = ILocation(model, None)
            if proxy is None:
                proxy = LocationProxy(model)

            id = self.key_reverse(model)
            locate(proxy, self, id)
            yield proxy

    def add(self, item):
        try:
            self.session.add(item)
        except Exception, e:
            # This might be a bit too generic
            return e

    def delete(self, item):
        self.session.delete(item)
