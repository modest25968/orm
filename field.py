class BaseField:
    sql_type = "None"


class CharField(BaseField):
    sql_type = "text"


class IntField(BaseField):
    sql_type = "int"

