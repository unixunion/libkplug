"""
    libkplug, a plugin system for python applications

    Copyright (C) 2013 Kegan Holtzhausen

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = 'Kegan Holtzhausen <marzubus@gmail.com>'

import inspect

"""
The plugin system
"""

import functools
import logging
from collections import OrderedDict

logging = logging.getLogger(__name__)


class KPluginClass(type):
    """This is a metaclass for construction only, see KPlugin rather"""

    def __new__(cls, clsname, bases, dct):
        new_object = super(KPluginClass, cls).__new__(cls, clsname, bases, dct)
        return new_object


class KPlugin(object):
    """This is the plugin core object where all plugins should extend from and register too.
    Plugin Example:
    .. doctest::
        :options: +SKIP
        >>> import libkplug
        >>> @libkplug.plugin_registry.register
        >>> class Bar(KPlugin):
        >>>     plugin_name = "BarPlugin"
        >>>     def __init__(self):
        >>>         pass
        >>>     # Instance methods work!
        >>>     def hello(self, name):
        >>>         print("Hello %s from %s" % (name, self))
        >>>     # Static methods work too!
        >>>     @staticmethod
        >>>     def gbye():
        >>>         print("Cheers!")
        >>> libkplug.plugin_registry('BarPlugin').hello("dude")
        >>> libkplug.plugin_registry('BarPlugin').gbye()
        >>> import pprint
        >>> pprint.pprint(dir(libkplug.plugin_registry('BarPlugin')))

    Plugin Instantiation:
    >>> import libkplug
    >>> import libksettings
    >>> import plugins.plugin_helloworld
    >>> libkplug.plugin_registry('HelloWorldPlugin').hello_world()
    'Hello World'
    """
    __metaclass__ = KPluginClass
    plugins = []
    plugins_dict = OrderedDict()
    plugin_name = "KPlugin"
    """ the plugin's name, override this in the derived class!"""
    exists = False

    def __init__(self, *args, **kwargs):
        logging.info("Plugin Init: %s, %s" % (args, kwargs))

    def register(self, object_class):
        """
        Registers a object with the plugin registry, typically used as a decorator.
        :param object_class: the class to register as a plugin
        Example:
            .. doctest::
                :options: +SKIP
                >>> @libkplug.plugin_registry.register
                >>> class Foo(KPlugin)
                >>> ...
        """
        logging.info("Registering Plugin id: %s from class: %s " % (object_class.plugin_name, object_class))
        o = object_class
        self.plugins.append(o)
        self.plugins_dict[object_class.plugin_name] = o

        # helper for sphinx to find docstrings
        def _d(fn):
            print("Sphinx helper")
            return functools.update_wrapper(object_class(fn), fn)

        functools.update_wrapper(_d, object_class)
        return _d

    def __call__(self, *args, **kwargs):
        """
        When you call the registry with the name of a plugin eg: 'NullPlugin', as the first arg, this returns the class
        from the plugin_registry. You can then instantiate the class in any way you need to.
        Example:
            >>> import libkplug
            >>> clazz = libkplug.plugin_registry("NullPlugin")
            >>> type(clazz)
        ""
        :param args: name of Plugin to return
        :param kwargs:
        :return: class
        """

        try:
            module = get_calling_module(point=2)
        except:
            module = "Unknown"

        try:
            module_parent = get_calling_module(point=3)
        except:
            module_parent = "Unknown"

        logging.info(self.plugins_dict)
        logging.info("Module %s->%s->%s" % (module_parent, module, args[0]))
        logging.info("Plugin Request: args: %s, kwargs: %s" % (args, kwargs))
        try:
            logging.info("Class: %s" % self.plugins_dict[args[0]])
            return self.plugins_dict[args[0]]
        except:
            logging.warning("No plugin named: %s found, available plugins are: %s" % (args[0], self.plugins_dict))
            logging.warning(
                "Please check the plugin is listed in the yaml config and that you have @libkplug.plugin_registry.register in the class")
            raise

    def set_exists(self, state):
        """set_exists is used as caching in order to cut down on SEMP queries to validate existence of items. For example,
        if you create a new VPN in "batch" mode, After the "create-vpn" XML is generated, set_exists is set to True so
        subsequent requests decorated with the `only_if_exists` will function correctly since set_exists states that the
        object will exist.
        :param state: the existence state of the object
        :type state: bool
        :return:
        """
        module = get_calling_module(point=3)
        logging.info("Calling module: %s, Setting Exists bit: %s" % (module, state))
        self.exists = state


def get_calling_module(point=2):
    """
    Return a module at a different point in the stack.
    :param point: the number of calls backwards in the stack.
    :return:
    """
    frm = inspect.stack()[point]
    function = str(frm[3])
    line = str(frm[2])
    modulepath = str(frm[1]).split('/')
    module = str(modulepath.pop())
    return "%s:%s" % (module, line)


logging.info("Initializing plugin architecture")
plugin_registry = KPlugin()
