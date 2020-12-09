import os
import json

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from apps.app import set_logging 

if os.environ['ENV'] == 'development':
    with open('config/db.json', 'r') as f:
        db_conf = json.load(f)['development']
elif os.environ['ENV'] =='test':
    with open('config/db.json', 'r') as f:
        db_conf = json.load(f)['test']

dialect = db_conf['url']['dialect']
driver = db_conf['url']['driver']
username = db_conf['url']['username']
password = db_conf['url']['password']
host = db_conf['url']['host']
port = db_conf['url']['port']
database = db_conf['url']['database']

database_url = f"{dialect}+{driver}://{username}:{password}@{host}:{port}/{database}?charset=utf8"

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

#sqlalchemyのloggingを更新
set_logging()
