#dispatcher to postgresql

import psycopg2
from db.disp import BaseDispatcher
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from simple_settings import settings
class PostgresDispatcher(BaseDispatcher):
    cur = None
    conn = None


    def __init__(self, namedb=None, dbusername=None):
        os.environ['SIMPLE_SETTINGS'] = "test_settings"
        if not namedb:
            namedb = settings.DB_NAME

        if not dbusername:
            dbusername = settings.DB_USERNAME

        self.conn = psycopg2.connect("dbname={0} user={1}".format(namedb, dbusername))
        self.createCursor()

    def __del__(self):
        self.closeConn()

    def closeConn(self):
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

    def createTestDB(self):
        self.closeConn()
        conn2 = psycopg2.connect("dbname=postgres user=postgres")
        conn2.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn2.cursor()

        cur.execute("DROP DATABASE IF EXISTS testdb")
        cur.execute("CREATE DATABASE testdb")
        cur.close()
        conn2.close()
        self.conn = psycopg2.connect("dbname=testdb user=postgres")
        self.createCursor()


    def createCursor(self):
        self.cur = self.conn.cursor()
