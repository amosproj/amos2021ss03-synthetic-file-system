import unittest

class TestDummy(unittest.TestCase):

    def test_one(self):
        self.assertTrue(42)

    def test_two(self):
        self.assertEqual("a", "a")


def test_dummy():
    assert("banana")