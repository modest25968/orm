import field
from model import BaseModel


class Users(BaseModel):
    fname = field.CharField()
    lname = field.CharField()
    lenOfPipi = field.IntField()


class Posts(BaseModel):
    text = field.CharField()

class Comment(BaseModel):
    text = field.CharField()