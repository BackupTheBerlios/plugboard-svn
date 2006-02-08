PlugBoard is an Application Framework made in Python built on top of
setuptools and zope interfaces which help the developer create a
plugin-based application.
The framework itself is very extensible and let the
application be extensible too as well. An application is made up of a plugin
resource (get all available plugins in the application), a context resource
(organize plugins into different contexts) and an engine to let plugins
communicate each other into different environments (such as PlugBoard, Gtk,
Wx, Qt, Twisted, and so on) and provide some useful utilities.

To start a new project using a basic file structure type:
$ plugboardctl.py create PROJECTNAME

More informations can be found at
http://developer.berlios.de/projects/plugboard/