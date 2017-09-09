import unittest
from utils import isFilesExist, findModelsAndFieldsInFiles

class TestUtils(unittest.TestCase):
    def testFileExist(self):
        self.assertTrue(isFilesExist(["testt/modelfortest.py", "utils.py"]))
        self.assertFalse(isFilesExist(["lol"]))

    def testFindModel(self):
        res = findModelsAndFieldsInFiles(["testt/modelfortest.py"])
        self.assertEqual(len(res), 2)
        sum = 0
        for key, val in res.items():
            sum += len(val)
        self.assertEqual(sum, 4)


if __name__ == '__main__':
    unittest.main()
