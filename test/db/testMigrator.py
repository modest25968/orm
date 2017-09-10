from db.migrator import Migrator
# from db.disp import Disp
import unittest
from utils import findModelsAndFieldsInFiles
from db.disp import Disp
from simple_settings import settings
import os

class TestMigrator(unittest.TestCase):
    @unittest.skip("demonstrating skipping")
    def testEscenceStructCreate(self):
        Disp().inst().createTestDB()
        tc = Migrator()
        tc.createStructEssenceTable()


    def testEscenceCreate(self):
        # testStructureCreate
        Disp().inst().createTestDB()
        tc = Migrator()
        tc.createStructEssenceTable()

        os.environ['SIMPLE_SETTINGS'] = "test_settings"
        escences = findModelsAndFieldsInFiles(settings.FILES_WITH_MODELS)

        # testInsert
        for essname, ess in escences.items():
            tc.insertEssenceInfoInEssencesTable((essname, ess))

        res = tc.getAllEssencesNames()
        self.assertEqual(len(res), 2)
        self.assertIsNotNone(tc.findRecordEssence("Posts"))
        self.assertIsNotNone(tc.findRecordEssence("Users"))

        for essname, fields in escences.items():
            tc.insertEssenceInfoInEssencesFieldsTable((essname, fields))

            tc.createEssenceTable((essname, fields))

        res = tc.getAllEssencesFromBd()
        print(res)
        print(escences)








if __name__ == '__main__':
    unittest.main()
