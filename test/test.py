import unittest


from testutils import TestUtils
from db.testpostDisp import TestPostgreDisp
from db.testSqlCreator import TestSqlCreator
from db.testMigrator import TestMigrator

if __name__ == "__main__":
    tl = unittest.TestLoader()
    tests = list()
    tests.append(tl.loadTestsFromTestCase(TestUtils))
    tests.append(tl.loadTestsFromTestCase(TestPostgreDisp))
    tests.append(tl.loadTestsFromTestCase(TestSqlCreator))
    tests.append(tl.loadTestsFromTestCase(TestMigrator))
    all_test = unittest.TestSuite(tests)
    unittest.TextTestRunner(verbosity=2).run(all_test)
