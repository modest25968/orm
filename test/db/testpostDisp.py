from db.postDisp import PostgresDispatcher

import unittest


class TestPostgreDisp(unittest.TestCase):
    def testDB(self):
        disp = PostgresDispatcher()# "testdb", "postgres")
        disp.createTestDB()
        disp.exec("CREATE TABLE test (id serial PRIMARY KEY, name text);")
        disp.exec("INSERT INTO  test (name) VALUES ('first')")
        text = disp.exec("SELECT * FROM test;", True)
        self.assertEqual(text, [(1, 'first')])
        disp.exec("DROP TABLE test")
        disp.commit()

if __name__ == '__main__':
    unittest.main()
