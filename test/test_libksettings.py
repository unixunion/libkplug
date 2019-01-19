
__author__ = 'Kegan Holtzhausen <marzubus@gmail.com>'

import os
import sys
from importlib import reload

sys.path.insert(1, os.path.join(sys.path[0], '../../src'))

import unittest
import libksettings

class UnitTests(unittest.TestCase):

    def setUp(self):
        pass


    def tearDown(self):
        reload(libksettings)

    def test_create(self):
        settings = libksettings.KSettings(A='a', b=1, c=True, PLUGINS=[])
        self.assertEqual(settings.A, 'a')
        self.assertEqual(settings.b, 1)
        self.assertEqual(settings.c, True)
        self.assertEqual(settings.KEY1, 'VAL1')

    def test_create_noconfig(self):
        settings2 = libksettings.KSettings(A='a', b=1, c=True, PLUGINS=[], load_yaml=False)
        self.assertEqual(settings2.A, 'a')
        self.assertEqual(settings2.b, 1)
        self.assertEqual(settings2.c, True)
        with self.assertRaises(KeyError):
            settings2.KEY1

    def test_create_pathed_config(self):
        settings = libksettings.KSettings(config_filename='test/other.yaml', A='a', b=1, c=True, PLUGINS=[])
        self.assertEqual(settings.A, 'a')
        self.assertEqual(settings.b, 1)
        self.assertEqual(settings.c, True)
        self.assertEqual(settings.KEY2, 'VAL2')

    def test_create_env_config(self):
        os.environ.setdefault('MY_CONF', 'test/other.yaml')
        settings = libksettings.KSettings(config_filename_envvar='MY_CONF', A='a', b=1, c=True, PLUGINS=[])
        self.assertEqual(settings.A, 'a')
        self.assertEqual(settings.b, 1)
        self.assertEqual(settings.c, True)
        self.assertEqual(settings.KEY2, 'VAL2')

    def test_global_accessability(self):
        settings1 = libksettings.KSettings(A='a', b=1, c=True, PLUGINS=[], load_yaml=False)
        settings2 = libksettings.KSettings(load_yaml=False)
        self.assertEqual(settings1.A, settings2.A)

if __name__ == "__main__":
    unittest.main()
