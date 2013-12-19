# -*- coding: utf-8 -*-

from cromlech.sqlalchemy import get_session
from zope.location import Location, LocationProxy, locate
from zope.interface import implementer
from .interfaces import ISQLContainer


@implementer(ISQLContainer)
class SQLContainer(Location):

    model = None
    key_converter = None

    def __init__(self, parent, name, db_key):
        self.__parent__ = parent
        self.__name__ = name
        self.db_key = db_key

    @property
    def session(self):
        return get_session(self.db_key)
        
    def __getitem__(self, id):
        if self.key_converter is not None:
            try:
                key = self.key_converter(id)
            except ValueError as e:
                raise KeyError(id)
        else:
            key = id

        model = self.session.query(self.model).get(key)
        
        if model is None:
            raise KeyError(key)
        proxy = LocationProxy(model)
        locate(proxy, self, str(id))
        return proxy

    def query_filters(self, query):
        return query
        
    def __iter__(self):
        models = self.query_filters(self.session.query(self.model))
        return iter([LocationProxy(model, self, str(model.id))
                     for model in models])

    def add(self, item):
        try:
            self.session.add(item)
        except Exception, e:
            # This might be a bit too generic
            return e

    def delete(self, item):
        self.session.delete(item)
