# Copyright (c) 2005-2006 Italian Python User Group
# See LICENSE.txt for details.

from zope import interface
from zope.interface import adapter
import pkg_resources, sys

class IApplication(interface.Interface):
    """
    Main application interface
    """

    plugins = interface.Attribute("A list of found PlugBoard plugins")

    def __init__(self):
        """
        Create an application and give the path where to search for plugin entries
        """

    def register(self, ofrom, oto, name=''):
        """
        Register adaption from ofrom object to oto object gaining automatically their interfaces
        """

class Application(object):
    interface.implements(IApplication)

    def __init__(self):
        self.registry = adapter.AdapterRegistry()
        interface.interface.adapter_hooks = [self._adapter_hook]

    def _adapter_hook(self, provided, obj):
        adapter = self.registry.lookup1(interface.providedBy(obj), provided, '')
        if callable(adapter):
            return adapter(obj)
        else:
            adapter.application = self
            return adapter

    def _get_interface(self, obj):
        try:
            if issubclass(obj, interface.Interface):
                return obj
        except:
            pass
        if callable(obj):
            return interface.implementedBy(obj)
        else:
            return interface.providedBy(obj)
            
    def register(self, ofrom, oto, name=''):
        self.registry.register([self._get_interface(ofrom)], self._get_interface(oto), name, oto)
