#dispatcher to postgresql

import psycopg2
from db.disp import BaseDispatcher


class PostgresDispatcher(BaseDispatcher):
    cur = None
    conn = None


    def __init__(self, namedb="testdb", dbusername="postgres"):
        self.conn = psycopg2.connect("dbname={0} user={1}".format(namedb, dbusername))
        self.createCursor()

    def __del__(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

    def exec(self, text, fetch=False):
        self.cur.execute(text)
        if fetch:
            return self.cur.fetchall()

    def commit(self):
        self.conn.commit()

    def createCursor(self):
        self.cur = self.conn.cursor()
