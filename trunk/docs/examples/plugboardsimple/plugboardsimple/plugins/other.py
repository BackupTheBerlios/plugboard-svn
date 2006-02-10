from zope.interface import implements
from plugboard import engine, plugin
from interfaces import *

# Some plugin

class SomePlugin(plugin.Plugin):
    implements(ISomePlugin)

    def preload(self, context):
        ICorePlugin(self.application).dispatcher['event'].connect(self.on_event)

    def on_event(self, plugin, data):
        print "- SomePlugin received 'event' containing %r" % data

# Other plugin

class CoreConnector(engine.EventConnector):
    def on_event(self, plugin, data):
        print "- OtherPlugin received 'event' containing %r" % data

class OtherPlugin(plugin.Plugin):
    implements(IOtherPlugin)

    def preload(self, context):
        CoreConnector(ICorePlugin(self.application)).connect_all()
