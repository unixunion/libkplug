
__author__ = 'Kegan Holtzhausen <marzubus@gmail.com>'

import os
import sys
import logging

logging.basicConfig(level=logging.WARN,
                    format='%(module)s %(filename)s:%(lineno)d %(asctime)s %(levelname)s %(message)s',
                    stream=sys.stdout)
logging.getLogger().setLevel(logging.INFO)

sys.path.insert(1, os.path.join(sys.path[0], '../../src'))

import unittest
from libkplug import KPlugin


class UnitTests(unittest.TestCase):

    def setUp(self):
        self.registry = KPlugin()

    def test_plugin_class_register(self):
        # initializes the plugin system
        import libkplug

        # a inline plugin registration
        @libkplug.plugin_registry.register
        class Bar(KPlugin):
            plugin_name = 'BarPlugin'

            def __init__(self, *args, **kwargs):
                logging.info('Instantiating instance of: %s args: %s and kwargs: %s' % (self.plugin_name, args, kwargs))

            def hello(self, name="default"):
                logging.info("Hello %s from %s instance method" % (name, self))
                return name

            @staticmethod
            def hello_world():
                logging.info("Hello World")
                return "Hello World"

        # static method test
        t1 = libkplug.plugin_registry('BarPlugin').hello_world()
        self.assertEqual(t1, "Hello World")

        # instantiated class method test
        clazz = libkplug.plugin_registry('BarPlugin')
        inst = clazz("arg1", "arg2", foo="bar", settings={'k': 'v'})
        t2 = inst.hello(name="dude")
        self.assertEqual(t2, "dude")


if __name__ == "__main__":
    logging = logging.getLogger(__name__)
    unittest.main()
