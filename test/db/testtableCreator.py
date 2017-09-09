from db.tableCreator import TableCreator
from db.disp import Disp
import unittest


class TestTableCreator(unittest.TestCase):
    def testEscenceCreate(self):
        #for i in range(2):
            d = Disp.inst()
            tc = TableCreator()
            tc.createEssenceTable(True)
            #d.exec()

if __name__ == '__main__':
    unittest.main()
