from plugboard import plugin
from zope.interface import implements
import interfaces, gtk

class MainWindowPlugin(plugin.Plugin):
  implements(interfaces.IMainWindowPlugin)

  def __init__(self, application):
    self.widget = gtk.Window()
    self.widget.set_title("PlugEditor")

  def load(self, context):
    self.widget.show_all()

  def get_widget(self):
    return self.widget
