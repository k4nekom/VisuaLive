import json

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


with open('config/db.json', 'r') as f:
    db_conf = json.load(f)['development']

dialect = db_conf['url']['dialect']
driver = db_conf['url']['driver']
username = db_conf['url']['username']
password = db_conf['url']['password']
host = db_conf['url']['host']
port = db_conf['url']['port']
database = db_conf['url']['database']

database_url = f"{dialect}+{driver}://{username}:{password}@{host}:{port}/{database}"

engine = create_engine(
    database_url, 
    echo = True, 
    pool_size = db_conf['engine']['pool_size'], 
    max_overflow = db_conf['engine']['max_overflow'],
    isolation_level = db_conf['engine']['isolation_level'],
)

Base = declarative_base()

session = scoped_session(sessionmaker(
    autocommit = False,
    autoflush = True,
    bind = engine
))

'''
SQLAlchemy Modelまたはクエリの実行結果の行オブジェクト（またはその配列）をdict（の配列）に変換
'''
def row_to_dict(rowobj):
    if '__dict__' in dir(rowobj):
        return rowobj.__dict__
    else:
        return dict(rowobj)

'''
SQLAlchemyのormオブジェクトまたはsqlの実行結果（またはその配列）をdict（の配列）に変換
'''
def to_dict(obj):  #obj = sqlalchemy or cursor objects
    if isinstance(obj, list):
        for r in obj:
            return [row_to_dict(r) for r in obj]
    else:
        # Cursor resultset Rows
        return row_to_dict(obj)

