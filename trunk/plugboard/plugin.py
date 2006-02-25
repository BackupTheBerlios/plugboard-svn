# Copyright (c) 2005-2006 Italian Python User Group
# See LICENSE.txt for details.

from zope import interface
import pkg_resources
import types, traceback

# Interfaces

class IPlugin(interface.Interface):
    """
    A basic interface for allkind of plugins
    """

    dispatcher = interface.Attribute("An IEventDispatcher object to let other plugins connect to the plugin trough events")
    application = interface.Attribute("Automatically set when initializing the plugin")
    context = interface.Attribute("Automatically set when loading the plugin into the current context")
    plugin = interface.Attribute("Automatically set when creating a new instance of the plugin to be plugged into another one")

    def preload(context):
        """
        Called before loading the plugin
        """

    def load(context):
        """
        Load plugin in the current context
        """       

    def plug(plugin):
        """
        Plug the plugin into another plugin
        """

    def unload(context):
        """
        Unload plugin from the current context
        """

    def unplug(plugin):
        """
        Unplug the plugin from another plugin
        """

class IPluginResource(interface.Interface):
    """
    Application plugin control which contains all available plugins
    """

    def get_plugins():
        """
        Returns the list of detected plugins
        """
    get_plugins.return_type = types.GeneratorType

    def refresh():
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
    def __init__(self, application, entrypoint_path):
        super(SetuptoolsPluginResource, self).__init__(application)
        self.entrypoint_path = entrypoint_path
        
    def refresh(self, entrypoint_path=None):
        if entrypoint_path is not None:
            self.entrypoint_path = entrypoint_path
        self._plugins.clear()
        for entrypoint in pkg_resources.iter_entry_points(self.entrypoint_path):
            try:
                plugin_class = entrypoint.load()
            except:
                traceback.print_exc()
                continue
            self._plugins.add(plugin_class)

__all__ = ['IPlugin', 'IPluginResource', 'Plugin', 'PluginResource']
