import field
from model import BaseModel


class User(BaseModel):
    fname = field.CharField()
    lname = field.CharField()
    lenOfPipi = field.IntField()

class post(BaseModel):
    text = field.CharField()
