import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '../../src'))

import unittest
from libksettings import KSettings

class UnitTests(unittest.TestCase):

    def setUp(self):
        pass

    def test_create(self):
        settings = KSettings(A='a', b=1, c=True, PLUGINS=[])
        self.assertEqual(settings.A, 'a')
        self.assertEqual(settings.b, 1)
        self.assertEqual(settings.c, True)


if __name__ == "__main__":
    unittest.main()