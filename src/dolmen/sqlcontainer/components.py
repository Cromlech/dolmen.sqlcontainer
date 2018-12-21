# -*- coding: utf-8 -*-

from zope.location import ILocation, Location, LocationProxy, locate
from zope.interface import implementer
from zope.interface.interfaces import ComponentLookupError
from .interfaces import ISQLContainer


@implementer(ISQLContainer)
class SQLContainer(Location):

    model = None

    def __init__(self, session_getter, parent=None, name=None):
        self.__parent__ = parent
        self.__name__ = name
        self.get_session = session_getter

    def key_reverse(self, obj):
        """Customize if the primary_key is not "id" or to plug in
        the wanted behavior.
        """
        return str(obj.id)

    def key_converter(self, id):
        """Customize to plug in the wanted behavior.
        """
        return int(id)

    @property
    def session(self):
        return self.get_session()

    def __getitem__(self, id):
        try:
            key = self.key_converter(id)
        except ValueError:
            return None

        model = self.query_filters(self.session.query(self.model)).get(key)
        if model is None:
            raise KeyError(key)

        if not ILocation.providedBy(model):
            model = LocationProxy(model)

        locate(model, self, self.key_reverse(model))
        return model

    def query_filters(self, query):
        return query

    def __iter__(self):
        models = self.query_filters(self.session.query(self.model))
        for model in models:
            if not ILocation.providedBy(model):
                model = LocationProxy(model)
            locate(model, self, self.key_reverse(model))
            yield model

    def __len__(self):
        return self.query_filters(self.session.query(self.model)).count()

    def slice(self, start, size):
        models = self.query_filters(
            self.session.query(self.model)).limit(size).offset(start)
        for model in models:
            if not ILocation.providedBy(model):
                model = LocationProxy(model)
            locate(model, self, self.key_reverse(model))
            yield model

    def add(self, item):
        try:
            self.session.add(item)
        except Exception as e:
            # This might be a bit too generic
            return e

    def delete(self, item):
        self.session.delete(item)
