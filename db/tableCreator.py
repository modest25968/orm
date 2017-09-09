from db.disp import Disp

class TableCreator:

    #run only once
    def createStructEssenceTable(self, withCommit=True):
        Disp.inst().exec("CREATE TABLE essences (id serial PRIMARY KEY, " +
                         "name text);")

        Disp.inst().exec("CREATE TABLE essences_fields (id serial PRIMARY KEY, " +
                         "essences_id int, name text, type text);")

        if withCommit:
            Disp.inst().commit()

    def createEssenceTable(self, withCommit=True):
        pass


