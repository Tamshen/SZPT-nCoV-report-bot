import datetime
from peewee import *

database_proxy = DatabaseProxy()


class BaseModel(Model):
    class Meta:
        database = database_proxy


class Status:
    normal  = 0
    stopped = 1
    removed = 2
    warning = 3


class User(BaseModel):
    id = AutoField()
    token = CharField(null=True, index=True)
    name = CharField(null=True)
    user_id = CharField(null=True)
    user_pwd = CharField(null=True)
    status = IntegerField(index=True, default=Status.normal)
    create_time = DateTimeField(default=datetime.datetime.now, index=True)
    latest_response_time = DateTimeField(null=True, index=True)
    update_time = DateTimeField(default=datetime.datetime.now, index=True)

    def save(self, *args, **kwargs):
        self.update_time = datetime.datetime.now()
        return super(User, self).save(*args, **kwargs)


def init_db():
    database_proxy.connect()
    # TODO
    database_proxy.create_tables([User])
