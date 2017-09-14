import unittest
import pyqremis


class Tests(unittest.TestCase):
    def testPass(self):
        self.assertEqual(True, True)

    def testVersionAvailable(self):
        x = getattr(pyqremis, "__version__", None)
        self.assertTrue(x is not None)


if __name__ == "__main__":
    unittest.main()
