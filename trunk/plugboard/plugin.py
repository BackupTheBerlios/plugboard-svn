# Copyright (c) 2005-2006 Italian Python User Group
# See LICENSE.txt for details.

from zope import interface
import pkg_resources
import types

# Interfaces

class IPlugin(interface.Interface):
    """
    A basic interface for allkind of plugins
    """

    dispatcher = interface.Attribute("An IEventDispatcher object to let other plugins connect to the plugin trough events")
    application = interface.Attribute("Automatically set when initializing the plugin")
    context = interface.Attribute("Automatically set when loading the plugin into the current context")
    plugin = interface.Attribute("Automatically set when creating a new instance of the plugin to be plugged into another one")

    def __init__(self, application):
        """
        Initialize plugin
        """

    def preload(self, context):
        """
        Called before loading the plugin
        """

    def load(self, context):
        """
        Load plugin in the current context
        """       

    def plug(self, plugin):
        """
        Plug the plugin into another plugin
        """

    def unload(self, context):
        """
        Unload plugin from the current context
        """

    def unplug(self, plugin):
        """
        Unplug the plugin from another plugin
        """

class IPluginResource(interface.Interface):
    """
    Application plugin control which contains all available plugins
    """

    def get_plugins(self):
        """
        Returns the list of detected plugins
        """
    get_plugins.return_type = types.GeneratorType

    def refresh(self):
        """
        Refresh the list of plugins
        """

# Implementations

class Plugin(object):
    interface.implements(IPlugin)

    def __init__(self, application):
        pass

    def preload(self, context):
        pass

    def load(self, context):
        pass

    def plug(self, plugin):
        pass

    def unload(self, context):
        pass

    def unplug(self, plugin):
        pass

class PluginResource(object):
    interface.implements(IPluginResource)

    def __init__(self, application):
        self.application = application
        self._plugins = set()
        application.register(application, self)

    def get_plugins(self):
        return iter(self._plugins)

    def refresh(self):
        raise NotImplementedError

# Plugins

class SetuptoolsPluginResource(PluginResource):
    _plugins = set()

    def __init__(self, application, plugins_path):
        super(SetuptoolsPluginResource, self).__init__(application)
        self.plugins_path = plugins_path
        
    def refresh(self, plugins_path=None):
        if plugins_path is not None:
            self.plugins_path = plugins_path
        self._plugins.clear()
        for entrypoint in pkg_resources.iter_entry_points(self.plugins_path):
            plugin_class = entrypoint.load()
            self._plugins.add(plugin_class)

__all__ = ['IPlugin', 'IPluginResource', 'Plugin', 'PluginResource']
