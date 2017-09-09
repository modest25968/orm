from db.postDisp import PostgresDispatcher

import unittest


class TestPostgreDisp(unittest.TestCase):
    def testDB(self):
        for i in range(2):
            self.disp = PostgresDispatcher("testdb", "postgres")
            self.disp.exec("CREATE TABLE test (id serial PRIMARY KEY, name text);")
            self.disp.exec("INSERT INTO  test (name) VALUES ('first')")
            text = self.disp.exec("SELECT * FROM test;", True)
            self.assertEqual(text, [(1, 'first')])
            self.disp.exec("DROP TABLE test")
            self.disp.commit()

if __name__ == '__main__':
    unittest.main()
