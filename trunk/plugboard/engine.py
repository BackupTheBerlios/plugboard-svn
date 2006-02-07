# Copyright (c) 2005-2006 Italian Python User Group
# See LICENSE.txt for details.

from zope import interface
from plugboard import plugin
from types import MethodType

class IEvent(interface.Interface):
    """
    Informations about an event, emitter and connector.
    """

    name = interface.Attribute("The name of the event")
    arguments = interface.Attribute("A list of tuples defining the type and the description of each argument, e.g.: [(str, 'A string'), (int, 'An int')]")

    def emit(self, *args):
        """
        Emits the event
        """

    def connect(self, callback, *extra):
        """
        Connect to this event
        """

class IEventConnector(interface.Interface):
    """
    This is a convenience interface to make an easy connection with IEventDispatcher
    """
    
class IEventDispatcher(interface.Interface):
    """
    Contains all events of a given object
    """

    events = interface.Attribute("A list of IEvent")

    def add_event(self, name, *args):
        """
        A wrap method to create an IEvent
        """

    def get_event(self, name):
        """
        Returns the event with the given name
        """

    def remove_event(self, name):
        """
        Removes the event which got the given name from events
        """

    def get_events(self):
        """
        Returns an iter of all events
        """

    def get_event_names(self):
        """
        Returns an iter of all event names
        """

    def __getitem__(self):
        """
        A wrap method to get_event
        """

    def __iter__(self):
        """
        A wrap method to get_events
        """

class IEngine(interface.Interface):
    """
    Rappresentation of the engine used by the application
    """

# Implementation

class Event(object):
    interface.implements(IEvent)

    def __init__(self, dispatcher):
        self.dispatcher = dispatcher

class EventConnector(object):
    interface.implements(IEventConnector)

    def __init__(self, plugin):
        self.plugin = plugin
        self.dispatcher = plugin.dispatcher
        for name in dir(self):
            value = getattr(self, name)
            if not name.startswith('_') and self.dispatcher.has_event(name) and isinstance(value, MethodType):
                self.dispatcher[name].connect(value)

class EventDispatcher(object):
    interface.implements(IEventDispatcher)

    def __init__(self, plugin):
        self.plugin = plugin
        self._events = {}

    def add_event(self, name, *args):
        if self.has_event(name):
            raise LookupError, "Event %r already exists in dispatcher %r" % (name, self)
        event = IEvent(self)
        event.name = name
        event.arguments = args
        self._events[name] = event

    def get_event(self, name):
        return self._events[name]

    def has_event(self, name):
        return self._events.has_key(name)

    def remove_event(self, name):
        del self._events[name]

    def get_events(self):
        return self._events.itervalues()

    def get_event_names(self):
        return self._events.iterkeys()

    __getitem__, __iter__ = get_event, get_events

class Engine(object):
    interface.implements(IEngine)

    def __init__(self, application):
        self.application = application
        application.register(application, self)

# GTK plugin

class GTKEvent(Event):
    interface.implements(IEvent)

    def emit(self, *args):
        self.dispatcher._gobject.emit(self.name, *args)

    def connect(self, callback, *extra):
        self.dispatcher._gobject.connect_object(self.name, callback, self.dispatcher.plugin, *extra)

class GTKEventDispatcher(EventDispatcher):
    def __init__(self, plugin):
        super(GTKEventDispatcher, self).__init__(plugin)
        self._create_gobject()

    def add_event(self, name, *args):
        super(GTKEventDispatcher, self).add_event(name, *args)
        self._create_gobject()

    def _create_gobject(self):
        import gobject
        __gsignals__ = {}
        for event in self:
            garguments = [gobject.TYPE_PYOBJECT]*len(event.arguments)
            __gsignals__[event.name] = (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, garguments)
        odict = {'__gsignals__': __gsignals__}
        self._gobject = type('_PluginEventGObject', (gobject.GObject,), odict)()
        
class GTKEngine(Engine):
    def __init__(self, application):
        super(GTKEngine, self).__init__(application)
        application.register(plugin.IPlugin, GTKEventDispatcher)
        application.register(GTKEventDispatcher, GTKEvent)
