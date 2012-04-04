import unittest2 as unittest
import mock


class TestFoo(unittest.TestCase):

    def test_bar(self):
        a = 1
        self.assertEquals(2, a)
