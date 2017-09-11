import unittest
from utils import isFilesExist, findModelsAndFieldsInFiles


class TestUtils(unittest.TestCase):
    def testFileExist(self):
        self.assertTrue(isFilesExist(["modelfortest.py"]))
        self.assertFalse(isFilesExist(["lol"]))

    def testFindModel(self):
        res = findModelsAndFieldsInFiles(["modelfortest.py"])
        self.assertEqual(len(res), 2)
        summ = 0
        for key, val in res.items():
            summ += len(val)
        self.assertEqual(summ, 4)


if __name__ == '__main__':
    unittest.main()
