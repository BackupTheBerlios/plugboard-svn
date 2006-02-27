# Copyright (c) 2005-2006 Italian Python User Group
# See LICENSE.txt for details.

from plugboard import application, plugin, context, engine
from plugboard.test import plugins
import unittest
from zope import interface
from xml.dom import minidom

class TestPlugBoard(unittest.TestCase):
    def setUp(self):
        self.app = application.Application()
        
    def _install_setuptools_pr(self):
        plugin.SetuptoolsPluginResource(self.app, 'plugboard.test').refresh()

    def _install_basic_cr(self):
        self.app.register(context.ContextResource, context.Context)
        context.ContextResource(self.app).add_context('test',
                                                      plugin.IPluginResource(self.app).get_plugins())

    def test_adaption(self):
        self.app.register(application.IApplication, plugins.TestPlugin)
        self.assert_(plugins.ITestPlugin(self.app).__class__, plugins.TestPlugin)
        self.app.register(self.app, plugins.TestPlugin)
        self.assert_(plugins.ITestPlugin(self.app).__class__, plugins.TestPlugin)
        test = plugins.TestPlugin(self.app)
        self.app.register(self.app, test)
        self.assert_(plugins.ITestPlugin(self.app), test)

    def test_setuptools_plugin_resource(self):
        self._install_setuptools_pr()
        pr = plugin.IPluginResource(self.app)
        pr.refresh()
        self.assert_(plugins.TestPlugin in pr.get_plugins())

    def test_basic_context_resource(self):
        self._install_setuptools_pr()
        self._install_basic_cr()
        cr = context.IContextResource(self.app)
        cr['test'].load()
        self.assertEqual(plugins.ITestPlugin(self.app).__class__, plugins.TestPlugin)
        cr['test'].load()
        self.assertEqual(plugins.ITestPlugin(self.app).__class__, plugins.TestPlugin)

    def test_dict_context_resource(self):
        self._install_setuptools_pr()
        contexts = {
            'test': ['plugboard.test.plugins.TestPlugin'],
        }
        cr = context.DictContextResource(self.app, contexts)
        cr.refresh()
        cr['test'].load()
        cr['test'].load()
        self.assertEqual(plugins.ITestPlugin(self.app).__class__, plugins.TestPlugin)
        cr['test'].load()
        self.assertEqual(plugins.ITestPlugin(self.app).__class__, plugins.TestPlugin)

    def test_xml_context_resource(self):
        self._install_setuptools_pr()
        xml = """<test>
<context name='test'>
  <plugin path='plugboard.test.plugins.TestPlugin' />
</context>
</test>"""
        cr = context.XMLContextResource(self.app, minidom.parseString(xml).documentElement)
        cr.refresh()
        cr['test'].load()
        self.assertEqual(plugins.ITestPlugin(self.app).__class__, plugins.TestPlugin)
        cr['test'].load()
        self.assertEqual(plugins.ITestPlugin(self.app).__class__, plugins.TestPlugin)

    def test_plugboard_engine(self):
        self._install_setuptools_pr()
        self._install_basic_cr()
        engine.PlugBoardEngine(self.app)
        cr = context.IContextResource(self.app)
        cr['test'].load()
        class EC(engine.EventConnector):
            received = None
            def on_test(self, *data):
                self.received = data
            on_test.extra = ('extra test',)
        p = plugins.ITestPlugin(self.app)
        ec = EC(p)
        ec.connect_all()
        p.dispatcher['test'].emit('plugboardengine test')
        self.assertEqual(ec.received, (p, 'plugboardengine test', 'extra test',))
        ec.received = None
        ec.disconnect_all()
        p.dispatcher['test'].emit('gtkengine test')
        self.assertEqual(ec.received, None)

    def test_shared_event_argument(self):
        self._install_setuptools_pr()
        self._install_basic_cr()
        engine.GTKEngine(self.app)
        cr = context.IContextResource(self.app)
        cr['test'].load()
        class EC(engine.EventConnector):
            received = None
            def on_test(self, plugin, data):
                self.received = data.get_value()
                data.set_value(self.received+'test')
        p = plugins.ITestPlugin(self.app)
        ec, ec2, ec3 = EC(p), EC(p), EC(p)
        ec.connect_all(); ec2.connect_all(); ec3.connect_all()
        sharg = engine.SharedEventArgument()
        sharg.set_value('')
        p.dispatcher['test'].emit(sharg)
        self.assertEqual((ec.received, ec2.received, ec3.received),
                         ('', 'test', 'testtest'))

    def test_gtk_engine(self):
        self._install_setuptools_pr()
        self._install_basic_cr()
        engine.GTKEngine(self.app)
        cr = context.IContextResource(self.app)
        cr['test'].load()
        class EC(engine.EventConnector):
            received = None
            def on_test(self, *data):
                self.received = data
            on_test.extra = ('extra test',)
        p = plugins.ITestPlugin(self.app)
        ec = EC(p)
        ec.connect_all()
        p.dispatcher['test'].emit('gtkengine test')
        self.assertEqual(ec.received, (p, 'gtkengine test', 'extra test',))
        ec.received = None
        ec.disconnect_all()
        p.dispatcher['test'].emit('gtkengine test',)
        self.assertEqual(ec.received, None)

def get_test_suite():
    return unittest.makeSuite(TestPlugBoard)

if __name__ == '__main__':
    unittest.main()
