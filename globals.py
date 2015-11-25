import psycopg2
from flask import g

def get_db_conn():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db

def connect_to_database():
    return psycopg2.connect(host="movies.cfgdweprellz.us-east-1.rds.amazonaws.com", port=5432, database="project", user="cis450", password="450movies")



