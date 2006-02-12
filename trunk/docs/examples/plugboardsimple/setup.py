from setuptools import setup, find_packages

setup(
    name="Plugboardsimple",
    version="0.1",
    description="A simple plugboard example",
    author="Lethalman",
    packages=find_packages(),
    entry_points="""
    [plugboardsimple.plugins]
    CorePlugin = plugboardsimple.plugins.core:CorePlugin
    AnotherCorePlugin = plugboardsimple.plugins.core:AnotherCorePlugin
    SomePlugin = plugboardsimple.plugins.other:SomePlugin
    OtherPlugin = plugboardsimple.plugins.other:OtherPlugin
    """,
    install_requires=["PlugBoard>=0.1.1"],
    )
