from db.disp import Disp


class SqlCreator:
    _escence_not_change = False
    _essence_dict = None

    _instance = None

    @staticmethod
    def inst():
        if not SqlCreator._instance:
            SqlCreator._instance = SqlCreator()
        return SqlCreator._instance

    def findRecordEssence(self, NameEssence):
        esc = self.getAllEssencesNames()
        if NameEssence in esc:
            return esc[NameEssence]
        return None

    def getAllTableNames(self):
        sql = "SELECT table_name FROM information_schema.tables where table_schema = 'public';"
        return Disp.inst().exec(sql, True)

    def createTestDB(self):
        Disp.inst().createTestDB()

    # run only once
    def createStructEssenceTable(self, withCommit=True):
        Disp.inst().exec("CREATE TABLE IF NOT EXISTS essences (id serial PRIMARY KEY, " +
                         "name text);")

        Disp.inst().exec("CREATE TABLE IF NOT EXISTS essences_fields (id serial PRIMARY KEY, " +
                         "essences_id int, name text, type text);")

        if withCommit:
            Disp.inst().commit()

    def getAllEssencesNames(self):
        if not self._escence_not_change:
            # TODO: db return strings. parser rewrite
            res = Disp.inst().exec("SELECT (name, id) FROM essences", True)
            res = map(lambda x: x[0].replace("(", "").replace(")", "").split(","), res)
            res = map(lambda x: (x[0], int(x[1])), res)

            self._essence_dict = dict(res)
            self._escence_not_change = True
        return self._essence_dict


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


    def insertEssenceInfoInEssencesFieldsTable(self, Essence, withCommit=True):
        tablename = Essence[0]
        fields = Essence[1]
        essences = self.getAllEssencesNames()

        sqlEssenceFieldAdd = ""
        for field in fields:
            sqlEssenceFieldAdd += "INSERT INTO essences_fields (essences_id, name, type) VALUES " + \
                                  "({0}, '{1}', '{2}');".format(essences[tablename], field[0], field[1].sql_type)

        Disp.inst().exec(sqlEssenceFieldAdd)

        if withCommit:
            Disp.inst().commit()

    def deleteEssenceFromDb(self, essname):

        essId = self.getAllEssencesNames()[essname]
        Disp.inst().exec("DELETE FROM essences WHERE id={0}".format(essId))
        Disp.inst().exec("DELETE FROM essences_fields WHERE essences_id={0}".format(essId))
        Disp.inst().exec("DROP TABLE {0}".format(essname))
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

        sqlEssenceTableCreate = "CREATE TABLE " + tablename + " (id serial PRIMARY KEY"

        for field in fields:
            sqlEssenceTableCreate += ", " + field[0]+" "+field[1].sql_type

        sqlEssenceTableCreate += ');'

        Disp.inst().exec(sqlEssenceTableCreate)
        if withCommit:
            Disp.inst().commit()

    def getAllEssencesFromDb(self):
        sql = "SELECT s.name, sf.name, sf.type FROM essences as s, essences_fields as sf \
               WHERE s.id = sf.essences_id"
        res = Disp.inst().exec(sql, True)
        # TODO: db return string. rewrite parser
        d = dict()
        for x in res:
            if x[0] in d:
                d[x[0]].append((x[1], x[2]))
            else:
                d[x[0]] = [(x[1], x[2])]
        return d
