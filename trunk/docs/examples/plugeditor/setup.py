from setuptools import setup, find_packages

setup(
    name="Plugeditor",
    version="0.1",
    description="Project description",
    author="Project author",
    packages=find_packages(),
    entry_points="""
    [plugeditor.plugins]
    MainWindowPlugin = plugeditor.plugins.core:MainWindowPlugin
    """,
    install_requires=["PlugBoard>=0.2"],
    )
