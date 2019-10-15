import time
import unittest
from hieupro.helpers.RandomGenerator import RandomGenerator


class MyTestCase(unittest.TestCase):

    def test_random_password(self):

        self.assertEqual(len(RandomGenerator.random_password()) > 6, True)

    def test_random_id(self):
        self.assertEqual(len(RandomGenerator.random_id()) > len(str(int(time.time()))), True)