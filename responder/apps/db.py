import json

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


dialect = 'mysql'
driver = 'mysqldb'
username = 'docker'
password = 'docker'
host = 'db-container'
port = 3306
database = 'development'
pool_size = 5
max_overflow = 10
isolation_level = 'READ UNCOMMITTED'

database_url = f"{dialect}+{driver}://{username}:{password}@{host}:{port}/{database}"
engine = create_engine(
    database_url, 
    echo = True, 
    pool_size = 5, 
    max_overflow = 10,
    isolation_level = 'READ UNCOMMITTED',
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

