from db.tableCreator import TableCreator
from db.disp import Disp
import unittest


class TestTableCreator(unittest.TestCase):
    def testEscenceCreate(self):
        tc = TableCreator()
        tc.createStructEssenceTable()

if __name__ == '__main__':
    unittest.main()
