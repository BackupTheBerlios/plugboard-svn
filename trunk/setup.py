#!/usr/bin/env python

from setuptools import setup, find_packages
import os

setup(
    name="PlugBoard",
    version="0.1",
    description="An application framework to create plugin-based applications",
    long_description="""PlugBoard is an Application Framework made in Python built on top of setuptools and zope interfaces which help the developer to create a plugin-based application. The framework itself is very extensible trough plugins and let the application be extensible too as well. An applicatio is made up of a plugin resource (get all available plugins in the application), a context resource (organize plugins into different contexts) and an engine to let plugins communicate each other into different environments (such as PlugBoard, Gtk, Wx, Qt, Twisted, and so on).""",
    license="MIT",
    author="Italian Python User Group",
    author_email='lethalman88@gmail.com',
    url='http://developer.berlios.de/projects/plugboard/',   
    packages=find_packages(),
    package_data={
                  'plugboard.skeleton': ['*.txt'],
    },
    entry_points="""
    [plugboard.test]
    TestPlugin = plugboard.test.plugins:TestPlugin
    """,
    scripts=['scripts/plugboardctl.py'],
    test_suite="plugboard.test.main.get_test_suite",
#    install_requires=["zope_interface>=3.0.0b1"],
    )
