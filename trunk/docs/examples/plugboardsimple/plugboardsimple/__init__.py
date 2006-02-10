from plugboard import application, plugin, context, engine

contexts = {'context1': ['plugboardsimple.plugins.core.CorePlugin',
                         'plugboardsimple.plugins.other.OtherPlugin',
                         'plugboardsimple.plugins.other.SomePlugin'],
            'context2': ['plugboardsimple.plugins.core.AnotherCorePlugin',
                         'plugboardsimple.plugins.other.OtherPlugin',
                         'plugboardsimple.plugins.other.SomePlugin']}

app = application.Application()
pr = plugin.SetuptoolsPluginResource(app, 'plugboardsimple.plugins')
pr.refresh()
cr = context.DictContextResource(app, contexts)
cr.refresh()
engine.PlugBoardEngine(app)

def run():
    print '* Loading context1'
    cr.get_context('context1').load()
    print '* Loading context2'
    cr.get_context('context2').load()
