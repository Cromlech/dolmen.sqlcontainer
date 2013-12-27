# -*- coding: utf-8 -*-

from zope.interface import Interface, Attribute


class ISQLContainer(Interface):

    model = Attribute("The model class")

    def add(item):
        """Add the given item to this container.
        """

    def delete(item):
        """Delete the given item from this container.
        """
