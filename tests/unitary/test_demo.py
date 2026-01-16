import unittest

from ecodev_core import SafeTestCase


class DemoTest(SafeTestCase):
    """
    Class demonstrating how to do a test
    """

    def test_average_data(self):
        """
        simple test method
        """

        self.assertEqual(5, 5)


if __name__ == '__main__':
    unittest.main()
