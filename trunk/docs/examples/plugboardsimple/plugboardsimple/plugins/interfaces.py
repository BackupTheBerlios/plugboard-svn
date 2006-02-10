from plugboard.plugin import IPlugin

"""
Application plugin interfaces
"""

class ICorePlugin(IPlugin):
    """
    Signals:
    * event
    - 1st argument: str, "A simple data string"
    """

class ISomePlugin(IPlugin):
    """
    Connects to ICorePlugin to log what happens there
    """
    
class IOtherPlugin(IPlugin):
    """
    Same as ISomePlugin but using EventConnector
    """
