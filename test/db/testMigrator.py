from db.migrator import Migrator
# from db.disp import Disp
import unittest
from utils import findModelsAndFieldsInFiles
from db.disp import Disp
from simple_settings import settings
import os

class TestMigrator(unittest.TestCase):
    def testEscenceStructCreate(self):
        Disp().inst().createTestDB()
        tc = Migrator()
        tc.createStructEssenceTable()

    def testEscenceCreate(self):
        Disp().inst().createTestDB()
        tc = Migrator()

        os.environ['SIMPLE_SETTINGS'] = "test_settings"

        tc.createStructEssenceTable(settings.FILES_WITH_MODELS)

        res = findModelsAndFieldsInFiles(settings.FILES_WITH_MODELS)
        tc.createEssenceTable(('post', res['post']))
        print(tc.findRecordEssence("post"))




if __name__ == '__main__':
    unittest.main()
