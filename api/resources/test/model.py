from peewee import CharField, IntegerField
from ..utils import PsqlBaseModel

class Test(PsqlBaseModel.PsqlBaseModel):
    test = CharField()
