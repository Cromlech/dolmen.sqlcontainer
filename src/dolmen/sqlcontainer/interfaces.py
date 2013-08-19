# -*- coding: utf-8 -*-

from zope.interface import Interface, Attribute


class ISQLContainer(Interface):

    model = Attribute("The model class")
    
    def add(item):
        """
        """

    def delete(item):
        """
        """
