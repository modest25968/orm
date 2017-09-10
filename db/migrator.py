from db.disp import Disp

class Migrator:
    _escence_not_change = False
    _escence_dict = None

    def createTestDB(self):
        Disp.inst().exec("CREATE TABLE IF NOT EXISTS essences (id serial PRIMARY KEY, " +
                         "name text);")
        Disp.inst().commit()

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
        return esc[NameEssence]

    def getAllEssencesNames(self):
        if not self._escence_not_change:
            #TODO: Поправить это говно (бд возвращает строку_
            res = Disp.inst().exec("SELECT (name, id) FROM essences", True)
            res = map(lambda x: x[0].replace("(", "").replace(")", "").split(","), res)
            res = map(lambda x: (x[0], int(x[1])), res)

            self._escence_dict = dict(res)
            self._escence_not_change = True
        return self._escence_dict

    def getAllEssencesFromBd(self):
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

    def insertEssenceInfoInEssencesTable(self, Essence, withCommit=True):
        tablename = Essence[0]
        Disp.inst().exec("INSERT INTO essences (name) VALUES ('{0}')".format(tablename))
        self._escence_not_change = False

        if withCommit:
            Disp.inst().commit()

    def insertEssenceInfoInEssencesFieldsTable(self, Essence, withCommit=True):
        tablename = Essence[0]
        fields = Essence[1]
        essences = self.getAllEssencesNames()


        sqlEssenceFieldAdd = ""
        for field in fields:
            sqlEssenceFieldAdd += "INSERT INTO essences_fields (essences_id, name, type) VALUES ({0}, '{1}', '{2}');".format(essences[tablename], field[0], field[1].sql_type)

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
