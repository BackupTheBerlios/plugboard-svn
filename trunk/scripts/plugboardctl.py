from optparse import OptionParser
import os, shutil
from pkg_resources import Requirement, resource_filename

class CreateCommand(object):
    def __init__(self, main):
        self.main = main
        self.skeleton_path = resource_filename(Requirement.parse('PlugBoard'), 'plugboard/skeleton')
        self.setup_tmpl = """from setuptools import setup, find_packages

setup(
    name="%(project_title)s",
    version="0.1",
    description="Project description",
    author="Project author",
    packages=find_packages(),
    entry_points=\"\"\"
    [%(project_name)s.plugins]
    
    \"\"\",
    install_requires=["PlugBoard>=0.1"],
    )
"""

    def run(self, options, args):
        if not args:
            self.main.parser.error('You must specify the name of the project to create')
        project_name = args[0]
        shutil.copytree(self.skeleton_path, project_name)
        project_path = os.path.abspath(project_name)
        os.rename(os.path.join(project_path, '_app_'), os.path.join(project_path, project_name))
        setup_py = self.setup_tmpl % {'project_name': project_name,
                                      'project_title': project_name.title()}
        setup = file(os.path.join(project_path, 'setup.py'), 'w')
        setup.write(setup_py)
        setup.close()
        os.unlink(os.path.join(project_path, '__init__.py'))
        for curdir, dirs, files in os.walk(project_path):
            for filename in files:
                if filename.endswith('.pyc'):
                    os.unlink(os.path.join(curdir, filename))

class Main(object):
    def __init__(self):
        self.parser = OptionParser()
        self.commands = {
            'CREATE': CreateCommand(self),
        }

    def run(self):
        options, args = self.parser.parse_args()
        if not args:
            self.parser.error('You must specify one of the following commands: CREATE')
        command = args[0].upper()
        if not self.commands.has_key(command):
            self.parser.error('Command %r not found' % command)
            sys.exit(-1)
        self.commands[command].run(options, args[1:])

if __name__ == '__main__':
    Main().run()
