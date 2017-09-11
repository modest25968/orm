import os
import logging

from db.sqlcreator import SqlCreator
from utils import findModelsAndFieldsInFiles
from simple_settings import LazySettings

class Migrator:
    def compareEssencesFromDbAndFromClass(self, EssenceFB, EssenceFC):
        deleteEssences = {}
        createEssences = {}
        chengeEssences = {}
        keysFb = EssenceFB.keys()
        keysFc = EssenceFC.keys()

        keysFbc = keysFb & keysFc

        for key in keysFbc:
            chenges = self.compareEssncesFields(EssenceFB[key], EssenceFC[key])
            if not chenges[0]==chenges[1]==chenges[2]==[]:
                chengeEssences[key] = chenges

        keysFBNotC = keysFb - keysFc
        for key in keysFBNotC:
            deleteEssences[key] = EssenceFB[key]

        keysFCnotB = keysFc - keysFb
        for key in keysFCnotB:
            createEssences[key] = EssenceFC[key]

        return createEssences, deleteEssences, chengeEssences


    def compareEssncesFields(self, FieldsFB, FieldsFC):
        deleteFields = []
        createFields = []
        changeFields = []

        fieldsFB = {key: val for key, val in FieldsFB}
        fieldsFC = {key: val for key, val in FieldsFC}

        keysFb = fieldsFB.keys()
        keysFc = fieldsFC.keys()

        keysFbc = keysFb & keysFc

        for key in keysFbc:
            if fieldsFB[key] != fieldsFC[key].sql_type:
                changeFields.append((key, fieldsFC[key]))

        keysFBNotC = keysFb - keysFc
        for key in keysFBNotC:
            deleteFields.append((key, fieldsFB[key]))

        keysFCnotB = keysFc - keysFb
        for key in keysFCnotB:
            createFields.append((key, fieldsFC[key]))

        return createFields, deleteFields, changeFields


    def migrate(self):
        logger = logging.getLogger()
        logger.info("START MIGRATE")
        print("START MIGRATE")
        sq = SqlCreator.inst()
        sq.createStructEssenceTable()
        #os.environ['SIMPLE_SETTINGS'] = "test_settings"
        settings = LazySettings()
        essencesFc = findModelsAndFieldsInFiles(settings.FILES_WITH_MODELS)
        essencesFb = sq.getAllEssencesFromDb()
        chenges = self.compareEssencesFromDbAndFromClass(essencesFb, essencesFc)

        #create essences on db
        for essname, fields in chenges[0].items():

            logger.info("CREATE TABLE " + essname)
            print("CREATE TABLE " + essname)
            sq.insertEssenceInfoInEssencesTable(essname)
            sq.insertEssenceInfoInEssencesFieldsTable((essname, fields))
            sq.createEssenceTable((essname, fields))
            logger.info("Fields: "+str(list(map(lambda x: x[0]+" "+x[1].sql_type+";", fields))))
            print("Fields: "+"".join(list(map(lambda x: x[0]+" "+x[1].sql_type+";", fields))))


        #delete essences from db
        for essname, fields in chenges[1].items():
            logger.info("DELETE TABLE " + essname)
            print("DELETE TABLE " + essname)
            sq.deleteEssenceFromDb(essname)

        #change essence
        for essname, fields in chenges[2].items():
            print("change migr!!!")
            print(essname, fields)
