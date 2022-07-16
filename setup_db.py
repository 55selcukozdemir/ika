import sqlite3

from flask import flash
from flask import g

DATABASE = "root/database/database.db"

def getDB ():
    db = getattr(g, '__database', None)
    if db is None:
        db = g.__database = sqlite3.connect(DATABASE)
    return db

def close_connection(exception):
    db = getattr(g, '__database', None)
    if db is not None: 
        db.close()