import sys

#from settings import DB_BACKEND
DB_BACKEND = "postgresql"

import django

class BaseDispatcher:
    def exec(self, text, fetch="false"):
        pass


# singleton
class Disp(object):
    __instance = None

    @staticmethod
    def inst():
        if not Disp.__instance:
            Disp.__instance = getDisp()
        return Disp.__instance


def getDisp():
    if DB_BACKEND == "postgresql":
        from db.postDisp import PostgresDispatcher
        return PostgresDispatcher()

    print("can't create db backend select DB_BACKEND")
    sys.exit()
    return None


