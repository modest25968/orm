class BaseField:
    sql_type = "None"
    default_val = None



class CharField(BaseField):
    def __init__(self, def_val=""):
        self.default_val = def_val
    sql_type = "text"


class IntField(BaseField):
    def __init__(self, def_val=0):
        self.default_val = def_val
    sql_type = "int"

