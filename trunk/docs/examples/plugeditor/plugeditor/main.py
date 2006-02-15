from plugboard import application, plugin

def main():
  app = application.Application()
  pr = plugin.SetuptoolsPluginResource(app, 'plugeditor.plugins')
  pr.refresh()
