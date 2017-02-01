# -*- coding: utf-8 -*-

from cromlech.sqlalchemy import get_session
from zope.location import ILocation, Location, LocationProxy, locate
from zope.interface import implementer
from zope.interface.interfaces import ComponentLookupError
from .interfaces import ISQLContainer


@implementer(ISQLContainer)
class SQLContainer(Location):

    model = None

    def __init__(self, parent, name, db_key):
        self.__parent__ = parent
        self.__name__ = name
        self.db_key = db_key

    def key_reverse(self, obj):
        return str(obj.id)

    def key_converter(self, id):
        return id

    @property
    def session(self):
        return get_session(self.db_key)

    def __getitem__(self, id):
        try:
            key = self.key_converter(id)
        except ValueError:
            return None
        model = self.session.query(self.model).get(key)
        if model is None:
            raise KeyError(key)

        try:
            proxy = ILocation(model)
        except ComponentLookupError:
            proxy = LocationProxy(model)
        locate(proxy, self, self.key_reverse(model))
        return proxy

    def query_filters(self, query):
        return query

    def __iter__(self):
        models = self.query_filters(self.session.query(self.model))
        for model in models:
            try:
                proxy = ILocation(model)
            except ComponentLookupError:
                proxy = LocationProxy(model)
            locate(proxy, self, self.key_reverse(model))
            yield proxy

    def __len__(self):
        return self.query_filters(self.session.query(self.model)).count()

    def slice(self, start, size):
       models = self.query_filters(
           self.session.query(self.model)).limit(size).offset(start)
       for model in models:
           try:
               proxy = ILocation(model)
           except ComponentLookupError:
               proxy = LocationProxy(model)
           locate(proxy, self, self.key_reverse(model))
           yield proxy

    def add(self, item):
        try:
            self.session.add(item)
        except Exception as e:
            # This might be a bit too generic
            return e

    def delete(self, item):
        self.session.delete(item)
