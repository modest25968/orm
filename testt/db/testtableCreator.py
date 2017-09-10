from db.tableCreator import TableCreator
from db.disp import Disp
import unittest
from utils import findModelsAndFieldsInFiles


class TestTableCreator(unittest.TestCase):
    # @unittest.skip("demonstrating skipping")
    def testEscenceStructCreate(self):
        tc = TableCreator()
        tc.createStructEssenceTable()

    # @unittest.skip("demonstrating skipping")
    def testEscenceCreate(self):
        tc = TableCreator()
        res = findModelsAndFieldsInFiles(["testt/modelfortest.py"])
        tc.createEssenceTable(('post', res['post']))
        print(tc.findRecordEssence("post"))




if __name__ == '__main__':
    unittest.main()
