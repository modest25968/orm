import os
import unittest

from simple_settings import settings

from db.disp import Disp
from db.sqlcreator import SqlCreator
from utils import findModelsAndFieldsInFiles


class TestSqlCreator(unittest.TestCase):
    def testDB(self):
        pass

    def test_essence_struct_create(self):
        Disp.inst().createTestDB()
        sq = SqlCreator.inst()
        sq.createStructEssenceTable()

    def testEscenceCreate(self):
        # testStructureCreate
        Disp.inst().createTestDB()
        sq = SqlCreator.inst()
        sq.createStructEssenceTable()

        os.environ['SIMPLE_SETTINGS'] = "test_settings"
        essencesFc = findModelsAndFieldsInFiles(settings.FILES_WITH_MODELS)

        # testInsert
        for essname, ess in essencesFc.items():
            sq.insertEssenceInfoInEssencesTable(essname)

        res = sq.getAllEssencesNames()
        self.assertEqual(len(res), 2)

        self.assertIsNotNone(sq.findRecordEssence("Posts"))
        self.assertIsNotNone(sq.findRecordEssence("Users"))
        sq.deleteEssenceInfoInEssencesTable("Posts")
        self.assertIsNone(sq.findRecordEssence("Posts"))
        sq.insertEssenceInfoInEssencesTable("Posts")

        for essname, fields in essencesFc.items():
            sq.insertEssenceInfoInEssencesFieldsTable((essname, fields))
            sq.createEssenceTable((essname, fields))


if __name__ == '__main__':
    unittest.main()
