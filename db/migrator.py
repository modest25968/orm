from db.disp import Disp
from utils import findModelsAndFieldsInFiles
from simple_settings import LazySettings
import os
import logging

class Migrator:
    _escence_not_change = False
    _escence_dict = None

    def createTestDB(self):
        Disp().inst().createTestDB()

    # run only once
    def createStructEssenceTable(self, withCommit=True):
        Disp.inst().exec("CREATE TABLE IF NOT EXISTS essences (id serial PRIMARY KEY, " +
                         "name text);")

        Disp.inst().exec("CREATE TABLE IF NOT EXISTS essences_fields (id serial PRIMARY KEY, " +
                         "essences_id int, name text, type text);")

        if withCommit:
            Disp.inst().commit()

    def findRecordEssence(self, NameEssence):
        esc = self.getAllEssencesNames()
        if NameEssence in esc:
            return esc[NameEssence]
        return None

    def getAllEssencesNames(self):
        if not self._escence_not_change:
            #TODO: Поправить это говно (бд возвращает строку_
            res = Disp.inst().exec("SELECT (name, id) FROM essences", True)
            res = map(lambda x: x[0].replace("(", "").replace(")", "").split(","), res)
            res = map(lambda x: (x[0], int(x[1])), res)

            self._escence_dict = dict(res)
            self._escence_not_change = True
        return self._escence_dict

    def getAllEssencesFromDb(self):
        sql = "SELECT s.name, sf.name, sf.type FROM essences as s, essences_fields as sf \
               WHERE s.id = sf.essences_id"
        res = Disp().inst().exec(sql, True)
        # склеивание строк
        # TODO: Найти способ работать со строками и словарями
        d = dict()
        for x in res:
            if x[0] in d:
                d[x[0]].append((x[1], x[2]))
            else:
                d[x[0]] = [(x[1], x[2])]
        return d

    def insertEssenceInfoInEssencesTable(self, EssenceName, withCommit=True):
        Disp.inst().exec("INSERT INTO essences (name) VALUES ('{0}')".format(EssenceName))
        self._escence_not_change = False

        if withCommit:
            Disp.inst().commit()

    def deleteEssenceInfoInEssencesTable(self, EssenceName, withCommit=True):
        Disp.inst().exec("DELETE FROM essences where essences.name='{0}'".format(EssenceName))
        self._escence_not_change = False

        if withCommit:
            Disp.inst().commit()



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

    def getAllTableNames(self):
        sql = "SELECT table_name FROM information_schema.tables where table_schema = 'public'  \
              AND table_catalog = 'testdb';"
        return Disp().inst().exec(sql, True)


    def migrate(self):
        logger = logging.getLogger()
        logger.info("START MIGRATE")
        print("START MIGRATE")

        self.createStructEssenceTable()
        #os.environ['SIMPLE_SETTINGS'] = "test_settings"
        settings = LazySettings()
        essencesFc = findModelsAndFieldsInFiles(settings.FILES_WITH_MODELS)
        essencesFb = self.getAllEssencesFromDb()
        chenges = self.compareEssencesFromDbAndFromClass(essencesFb, essencesFc)

        #create essences on db
        for essname, fields in chenges[0].items():

            logger.info("CREATE TABLE " + essname)
            print("CREATE TABLE " + essname)
            self.insertEssenceInfoInEssencesTable(essname)
            self.insertEssenceInfoInEssencesFieldsTable((essname, fields))
            self.createEssenceTable((essname, fields))
            logger.info("Fields: "+str(list(map(lambda x: x[0]+" "+x[1].sql_type+";", fields))))
            print("Fields: "+"".join(list(map(lambda x: x[0]+" "+x[1].sql_type+";", fields))))


        #delete essences from db
        for essname, fields in chenges[1].items():
            logger.info("DELETE TABLE " + essname)
            print("DELETE TABLE " + essname)
            self.deleteEssenceFromDb(essname)

        #change essence
        for essname, fields in chenges[2].items():
            print("change migr!!!")
            print(essname, fields)

    def insertEssenceInfoInEssencesFieldsTable(self, Essence, withCommit=True):
        tablename = Essence[0]
        fields = Essence[1]
        essences = self.getAllEssencesNames()

        sqlEssenceFieldAdd = ""
        for field in fields:
            sqlEssenceFieldAdd += "INSERT INTO essences_fields (essences_id, name, type) VALUES ({0}, '{1}', '{2}'); \
                                  ".format(essences[tablename], field[0], field[1].sql_type)

        Disp.inst().exec(sqlEssenceFieldAdd)

        if withCommit:
            Disp.inst().commit()

    def deleteEssenceFromDb(self, essname):

        essId = self.getAllEssencesNames()[essname]
        Disp().inst().exec("DELETE FROM essences WHERE id={0}".format(essId))
        Disp().inst().exec("DELETE FROM essences_fields WHERE essences_id={0}".format(essId))
        Disp().inst().exec("DROP TABLE {0}".format(essname))
        self.deleteEssenceInfoInEssencesTable(essname)



    def deleteEssenceInfoInEssencesFieldsTable(self, essence, withCommit=True):
        tablename = essence[0]
        fields = essence[1]
        essences = self.getAllEssencesNames()

        sqlEssenceFieldAdd = ""
        for field in fields:
            sqlEssenceFieldAdd += "DELETE FROM essences_fields WHERE name='{0}'; \
                                  ".format(field[0])

        Disp.inst().exec(sqlEssenceFieldAdd)

        if withCommit:
            Disp.inst().commit()


    def createEssenceTable(self, Essence, withCommit=True):
        tablename = Essence[0]
        fields = Essence[1]

        sqlEssenceTableCreate = "CREATE TABLE " + tablename + "(id serial PRIMARY KEY"

        for field in fields:
            sqlEssenceTableCreate += ", " + field[0]+" "+field[1].sql_type

        sqlEssenceTableCreate += ');'

        Disp.inst().exec(sqlEssenceTableCreate)
        if withCommit:
            Disp.inst().commit()
