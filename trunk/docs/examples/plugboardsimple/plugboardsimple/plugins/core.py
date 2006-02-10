from zope.interface import implements
from interfaces import *
from plugboard import engine, plugin

# Core plugins

class BaseCorePlugin(plugin.Plugin):
    implements(ICorePlugin)

    def __init__(self, application):
        self.dispatcher = engine.IEventDispatcher(self)
        self.dispatcher.add_event('event', (str, 'Some data'))

class CorePlugin(BaseCorePlugin):
    def load(self, context):
        self.dispatcher['event'].emit("I'm CorePlugin from %s" % context.name)

class AnotherCorePlugin(BaseCorePlugin):
    def load(self, context):
        self.dispatcher['event'].emit("I'm AnotherCorePlugin from %s" % context.name)
