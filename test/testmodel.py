import field
from model import BaseModel


class MyModel(BaseModel):
    fname = field.CharField()
    lname = field.CharField()
    lenOfPipi = field.IntField()


