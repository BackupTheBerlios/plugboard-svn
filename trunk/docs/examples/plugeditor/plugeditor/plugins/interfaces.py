from plugboard.plugin import IPlugin
import gtk

class IMainWindowPlugin(IPlugin):
    def get_window():
        """
        Returns the main window widget
        """
    get_window.return_type = gtk.Window
