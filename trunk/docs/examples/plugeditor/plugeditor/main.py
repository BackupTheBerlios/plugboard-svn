from plugboard import application, plugin, context
import user, os
from xml.dom import minidom
import gtk

config_file = os.path.join(user.home, '.plugeditor')

def get_config():
  if not os.path.exists(config_file):
    file(config_file, 'w').write('<plugeditor />')
  try:
    return minidom.parse(config_file).documentElement
  except:
    pass

def main():
  app = application.Application()
  pr = plugin.SetuptoolsPluginResource(app, 'plugeditor.plugins')
  pr.refresh()
  config = get_config()
  if not config:
    print >> sys.stderr, "No valid configuration file as been found"
  cr = context.XMLContextResource(app, config)
  cr.refresh()
  cr['default'].load()
  gtk.main()
