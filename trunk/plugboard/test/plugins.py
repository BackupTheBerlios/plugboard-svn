from plugboard import plugin, engine
from zope import interface
import sys

class ITestPlugin(plugin.IPlugin):
    """
    Test
    """
    
class TestPlugin(plugin.Plugin):
    interface.implements(ITestPlugin)

    def __init__(self, application):
        try:
            self.dispatcher = engine.IEventDispatcher(self)
            self.dispatcher.add_event('test', (str, 'test data'))
        except TypeError:
            pass
