from peewee import *

database_proxy = DatabaseProxy()


class BaseModel(Model):
    class Meta:
        database = database_proxy


class ApiUser(BaseModel):
    id = AutoField()
    username = CharField()


def init_db():
    database_proxy.connect()
    # TODO
    database_proxy.create_tables([ApiUser])
