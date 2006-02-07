PlugBoard is an Application Framework made in Python built on top of
setuptools and zope interfaces which help the developer create a
plugin-based application.
The framework itself is very extensible trough plugins and let the
application be extensible too as well. An applicatio is made up of a plugin
resource (get all available plugins in the application), a context resource
(organize plugins into different contexts) and an engine to let plugins
communicate each other into different environments (such as PlugBoard, Gtk,
Wx, Qt, Twisted, and so on).