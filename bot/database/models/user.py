from peewee import *
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

db = SqliteDatabase(BASE_DIR/'users.db')

def init_users_table():
    """!DROPS! and inits current users table."""
    SchemaManager(Users, db).drop_table()
    Users.create_table()

def user_set_rank(uid, uname, new_rank):
    u = Users.select().where(Users.user_id == uid)

    if len(u) == 0:
        Users.create(user_id=uid, name=uname, rank=new_rank)
    
    Users.update(rank=new_rank).where(Users.user_id == uid).execute()

def user_get_rank(uid):
    u = Users.select().where(Users.user_id == uid)

    if len(u) == 0:
        return 0
    
    return u.get().rank

def get_top_ranks():
    top = Users.select().order_by(Users.rank.desc()).limit(10)
    
    tops = [(u.name, u.rank) for u in top]

    return tops

class Users(Model):
    user_id = BigIntegerField(unique=True)
    name = CharField()
    rank = IntegerField()

    class Meta:
        database = db

if __name__ == '__main__':
    init_users_table()