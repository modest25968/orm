from db.disp import Disp


class TableCreator:
    # run only once
    def createStructEssenceTable(self, withCommit=True):
        Disp.inst().exec("CREATE TABLE IF NOT EXISTS essences (id serial PRIMARY KEY, " +
                         "name text);")

        Disp.inst().exec("CREATE TABLE IF NOT EXISTS essences_fields (id serial PRIMARY KEY, " +
                         "essences_id int, name text, type text);")

        if withCommit:
            Disp.inst().commit()

    def findRecordEssence(self, NameEssence):
        res = Disp.inst().exec("SELECT * FROM essences where name=('{0}');".format(NameEssence), True)
        if not res:
            return
        if len(res) > 1:
            print("WARNING FIND MORE ONE")
        return res[0][0]

    def createEssenceTable(self, Essence, withCommit=True):
        tablename = Essence[0]

        Disp.inst().exec("INSERT INTO essences (name) VALUES ('{0}')".format(tablename))
        fields = Essence[1]

        sql = "CREATE TABLE " + tablename + "(id serial PRIMARY KEY,"
        for field in fields:
            sql += field[0]+" "+field[1].sql_type
        sql += ');'

        Disp.inst().exec(sql)
        if withCommit:
            Disp.inst().commit()
