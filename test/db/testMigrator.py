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
        # testStructureCreate
        Disp().inst().createTestDB()
        mig = Migrator()
        mig.createStructEssenceTable()

        os.environ['SIMPLE_SETTINGS'] = "test_settings"
        essencesFc = findModelsAndFieldsInFiles(settings.FILES_WITH_MODELS)

        # testInsert
        for essname, ess in essencesFc.items():
            mig.insertEssenceInfoInEssencesTable(essname)

        res = mig.getAllEssencesNames()
        self.assertEqual(len(res), 2)

        self.assertIsNotNone(mig.findRecordEssence("Posts"))
        self.assertIsNotNone(mig.findRecordEssence("Users"))
        mig.deleteEssenceInfoInEssencesTable("Posts")
        self.assertIsNone(mig.findRecordEssence("Posts"))
        mig.insertEssenceInfoInEssencesTable("Posts")

        for essname, fields in essencesFc.items():
            mig.insertEssenceInfoInEssencesFieldsTable((essname, fields))
            mig.createEssenceTable((essname, fields))



    def testCompareEssences(self):
        Disp().inst().createTestDB()
        mig = Migrator()
        os.environ['SIMPLE_SETTINGS'] = "test_settings"

        mig.createStructEssenceTable()

        essencesFc = findModelsAndFieldsInFiles(settings.FILES_WITH_MODELS)

        for essname, fields in essencesFc.items():
            mig.insertEssenceInfoInEssencesTable(essname)
            mig.insertEssenceInfoInEssencesFieldsTable((essname, fields))
            mig.createEssenceTable((essname, fields))
        # test equal
        essencesFc = findModelsAndFieldsInFiles(settings.FILES_WITH_MODELS)
        essencesFb = mig.getAllEssencesFromDb()

        chenges = mig.compareEssencesFromDbAndFromClass(essencesFb, essencesFc)
        for dic in chenges:
            self.assertFalse(dic)

        # test Fb more
        essencesFc = findModelsAndFieldsInFiles(settings.FILES_WITH_MODELS)
        essencesFb = mig.getAllEssencesFromDb()

        del essencesFb["Users"]
        chenges = mig.compareEssencesFromDbAndFromClass(essencesFb, essencesFc)

        self.assertTrue(chenges[0])
        self.assertFalse(chenges[1])
        self.assertFalse(chenges[2])
        self.assertTrue("Users" in chenges[0])
        self.assertEqual(len(chenges[0]["Users"]), 3)

        # test Fc more
        essencesFc = findModelsAndFieldsInFiles(settings.FILES_WITH_MODELS)
        essencesFb = mig.getAllEssencesFromDb()

        del essencesFc["Users"]
        chenges = mig.compareEssencesFromDbAndFromClass(essencesFb, essencesFc)

        self.assertFalse(chenges[0])
        self.assertTrue(chenges[1])
        self.assertFalse(chenges[2])
        self.assertTrue("Users" in chenges[1])
        self.assertEqual(len(chenges[1]["Users"]), 3)

        # test more field in class
        essencesFc = findModelsAndFieldsInFiles(settings.FILES_WITH_MODELS)
        essencesFb = mig.getAllEssencesFromDb()

        essencesFb["Users"].pop()
        essencesFb["Users"].pop()
        chenges = mig.compareEssencesFromDbAndFromClass(essencesFb, essencesFc)

        self.assertFalse(chenges[0])
        self.assertFalse(chenges[1])
        self.assertTrue(chenges[2])
        self.assertTrue("Users" in chenges[2])

        self.assertTrue(chenges[2]["Users"][0])
        self.assertFalse(chenges[2]["Users"][1])
        self.assertFalse(chenges[2]["Users"][2])

        self.assertEqual(len(chenges[2]["Users"][0]), 2)

        # test more field in db
        essencesFc = findModelsAndFieldsInFiles(settings.FILES_WITH_MODELS)
        essencesFb = mig.getAllEssencesFromDb()

        essencesFc["Users"].pop()
        essencesFc["Users"].pop()
        chenges = mig.compareEssencesFromDbAndFromClass(essencesFb, essencesFc)

        self.assertFalse(chenges[0])
        self.assertFalse(chenges[1])
        self.assertTrue(chenges[2])
        self.assertTrue("Users" in chenges[2])

        self.assertFalse(chenges[2]["Users"][0])
        self.assertTrue(chenges[2]["Users"][1])
        self.assertFalse(chenges[2]["Users"][2])

        self.assertEqual(len(chenges[2]["Users"][1]), 2)

        # test change field
        essencesFc = findModelsAndFieldsInFiles(settings.FILES_WITH_MODELS)
        essencesFb = mig.getAllEssencesFromDb()

        # change type of one field
        essencesFb['Users'][0] = (essencesFb['Users'][0][0], "None")

        chenges = mig.compareEssencesFromDbAndFromClass(essencesFb, essencesFc)

        self.assertFalse(chenges[0])
        self.assertFalse(chenges[1])
        self.assertTrue(chenges[2])
        self.assertTrue("Users" in chenges[2])

        self.assertFalse(chenges[2]["Users"][0])
        self.assertFalse(chenges[2]["Users"][1])
        self.assertTrue(chenges[2]["Users"][2])

        self.assertEqual(len(chenges[2]["Users"][2]), 1)

    def testMigrate(self):
        Disp().inst().createTestDB()
        mig = Migrator()
        mig.migrate()
        import os
        self.assertEqual(len(mig.getAllTableNames()), 4)
        os.environ['SIMPLE_SETTINGS'] = "test_settings_with_model2"
        mig.migrate()
        self.assertEqual(len(mig.getAllTableNames()), 5)
        os.environ['SIMPLE_SETTINGS'] = "test_settings"
        mig.migrate()
        self.assertEqual(len(mig.getAllTableNames()), 4)
        os.environ['SIMPLE_SETTINGS'] = "test_settings_with_model3"
        mig.migrate()
        self.assertEqual(len(mig.getAllTableNames()), 4)
        os.environ['SIMPLE_SETTINGS'] = "test_settings"
        mig.migrate()
        self.assertEqual(len(mig.getAllTableNames()), 4)

#        settings["FILES_WITH_MODELS"] = ["modelfortestwithnewclass.py"]

if __name__ == '__main__':
    unittest.main()
