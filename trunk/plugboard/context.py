# Copyright (c) 2005-2006 Italian Python User Group
# See LICENSE.txt for details.

from zope import interface
from xml.dom import minidom
from plugboard import plugin
import types

class IContext(interface.Interface):
    """
    A context is a container of plugins which are the working environment of the application
    """

    name = interface.Attribute("The name of the context")

    def add_plugins(plugins):
        """
        Add a new set of IPlugin classes to the context
        """

    def remove_plugins(plugins):
        """
        Remove the given set of IPlugin classes
        """

    def get_plugins():
        """
        Returns the set of IPlugin classes
        """
    get_plugins.return_type = types.GeneratorType
    
    def clear():
        """
        Clear all context plugin list
        """

    def load():
        """
        Unload working context, and load plugins
        """

    def unload():
        """
        Unload context plugins only if this is the working context
        """

class IContextResource(interface.Interface):
    """
    Application context control which contains all available contexts
    """

    current = interface.Attribute("Current loaded context")

    def add_context(name, plugins):
        """
        Add a new context to this resource and return it
        """
    add_context.return_type = IContext

    def get_context(name):
        """
        Returns the context with the given name
        """
    get_context.return_type = IContext

    def remove_context(name):
        """
        Remove the context with the given name
        """

    def get_context_names():
        """
        Returns a list of context names
        """
    get_context_names.return_type = types.GeneratorType

    def get_contexts():
        """
        Returns a list of all contexts
        """
    get_contexts.return_type = types.GeneratorType

    def clear():
        """
        Remove all contexts
        """

    def refresh():
        """
        Reload contexts
        """

    def __getitem__():
        """
        A wrap method to get_context
        """
    __getitem__.return_type = IContext

    def __iter__():
        """
        A wrap method to get_contexts
        """
    __iter__.return_type = types.GeneratorType

# Implementation

class Context(object):
    interface.implements(IContext)

    def __init__(self, resource):
        self.resource = resource
        self._plugins = set()
        self._loaded = set()

    def add_plugins(self, plugins):
        self._plugins.update(plugins)

    def remove_plugins(self, plugins):
        self._plugins.difference_update(plugins)

    def get_plugins(self):
        return iter(self._plugins)

    def clear(self):
        for i in xrange(len(self._plugins)):
            del self._plugins[i]

    def load(self):
        app = self.resource.application
        if self.resource.current:
            self.resource.current.unload()
        self._loaded.clear()
        for plugin in self._plugins:
            plugin.application = app
            plugin_instance = plugin(app)
            app.register(app, plugin_instance)
            self._loaded.add(plugin_instance)
        self.resource.current = self
        for plugin in self._loaded:
            plugin.preload(self)
        for plugin in self._loaded:
            plugin.load(self)
            plugin.context = self

    def unload(self):
        if self.resource.current == self:
            for plugin in self._loaded:
                plugin.unload(self)
            self.resource.current = None

class ContextResource(object):
    interface.implements(IContextResource)

    def __init__(self, application):
        self.application = application
        self._contexts = {}
        self.current = None
        application.register(application, self)

    def add_context(self, name, plugins):
        if self._contexts.has_key(name):
            raise KeyError, 'Context %r is already in this resource' % name
        ctx = IContext(self)
        ctx.name = name
        ctx.add_plugins(plugins)
        self._contexts[name] = ctx
        return ctx

    def get_context(self, name):
        return self._contexts[name]

    def remove_context(self, name):
        del self._contexts[name]

    def get_context_names(self):
        return self._contexts.iterkeys()

    def get_contexts(self):
        return self._contexts.itervalues()

    def clear(self):
        self._contexts.clear()

    def refresh(self):
        pass

    __getitem__, __iter__ = get_context, get_contexts

# Dict Plugin
class DictContextResource(ContextResource):
    def __init__(self, application, dict=None):
        """
        Retrieve contexts from the given dict, e.g.:
        dict = {'context_name': ['package.plugins.PluginClass', ...], ...}
        """
        super(DictContextResource, self).__init__(application)
        application.register(self, Context)
        self.dict = dict

    def refresh(self, dict=None):
        self._contexts.clear()
        if dict:
            self.dict = dict
        plugins_res = plugin.IPluginResource(self.application)
        for context_name, plugin_names in self.dict.iteritems():
            plugins_list = set()
            for plugin_name in plugin_names:
                for plg in plugins_res.get_plugins():
                    if plg.__module__+'.'+plg.__name__ == plugin_name:
                        plugins_list.add(plg)
            self.add_context(context_name, plugins_list)

# XML Plugin

class XMLContext(Context):
    dom_element = None

class XMLContextResource(ContextResource):
    def __init__(self, application, dom_element=None, context_element='context', context_name='name',
                 plugin_element='plugin', plugin_path='path'):
        """
        * dom_element xml.dom.minidom.Element: Element containing all contexts
        * context_element str: The name of the element of each context
        * context_name str: The attribute contained in the context element to retrieve the name of the context
        * plugin_element str: The name of the plugin sub elements for each context
        * plugin_path str: The path of the plugin, e.g.: plugexample.plugins.ExamplePlugin
        """
        super(XMLContextResource, self).__init__(application)
        application.register(self, XMLContext)
        self.dom_element = dom_element
        self.context_element = context_element
        self.context_name = context_name
        self.plugin_element = plugin_element
        self.plugin_path = plugin_path        

    def refresh(self, dom_element=None):
        self._contexts.clear()
        if dom_element:
            self.dom_element = dom_element
        plugin_res = plugin.IPluginResource(self.application)
        for node in self.dom_element.childNodes:
            if isinstance(node, minidom.Element) and node.tagName == self.context_element:
                if node.attributes.has_key(self.context_name):
                    ctx_name = node.attributes[self.context_name].value
                    ctx = IContext(self)
                    ctx.name = ctx_name
                    ctx.dom_element = node
                    self._contexts[ctx_name] = ctx
                    for subnode in node.childNodes:
                        if isinstance(subnode, minidom.Element) and subnode.tagName == self.plugin_element:
                            if subnode.attributes.has_key(self.plugin_path):
                                for plg in plugin_res.get_plugins():
                                    if subnode.attributes[self.plugin_path].value == plg.__module__+'.'+plg.__name__:
                                        ctx.add_plugins([plg])
