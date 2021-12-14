from enum import unique
from os import truncate
from peewee import *
import datetime
import os
from playhouse.db_url import connect


from flask_login import UserMixin
from peewee import database_required

# DATABASE = SqliteDatabase('places.sqlite')
DATABASE = connect(os.environ.get('DATABASE_URL') or 'sqlite:///places.sqlite')
class User(UserMixin, Model):
    username=CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()
    
    class Meta:
        database = DATABASE
        
from flask_login import UserMixin

class Favorite(Model):
    username = ForeignKeyField(User, backref='favoriteplaces')
    url = CharField()
    place = CharField()
    city = CharField()
    country = CharField()
    type = CharField()
    latitude = DecimalField()
    longitude = DecimalField()
    
    
    class Meta:
        database = DATABASE
        
class POI(Model):
    username = ForeignKeyField(User, backref='pointsofinterest')
    latitude = DecimalField()
    longitude = DecimalField()
    
    class Meta:
        database = DATABASE
    
    
    
def initialize(): 
    DATABASE.connect() 
    DATABASE.create_tables([User, Favorite, POI], safe=True)
    print("Connected to the DB and created tables if they don't already exist")
    # with SQL, don't leave DB connection open, we don't want to hog space in the connection pool
    DATABASE.close()
    
    