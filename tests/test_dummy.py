import unittest


class TestDummy(unittest.TestCase):

    def test_one(self) -> None:
        self.assertTrue(42)

    def test_two(self) -> None:
        self.assertEqual("a", "a")


def test_dummy() -> None:
    assert("banana")
