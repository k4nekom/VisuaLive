import json

import pytest
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from apps.db import Base, engine
from videos.models import VideoData

@pytest.fixture(scope="function")
def session():
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

    Base.metadata.create_all(engine)

    session = scoped_session(sessionmaker(
        autocommit = False,
        autoflush = True,
        bind = engine
    ))

    yield session
    
    session.query(VideoData).delete()
    session.commit()


class TestModelVideoInfo:
    def test_valid_insert(self, session):
        videoData = VideoData(
            username = 'masaki',
            title = 'testだよ',
            broadcasted_at = '2020-09-13T14:15:18Z',
            url = 'https://www.twitch.tv/videos/739949384',
            channel_url = 'https://www.twitch.tv/videos/739949384',
            duration_minutes = 30,
            w_count = '[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]',
            comment_count = '[9, 8, 7, 6, 5, 4, 3, 2, 1, 0]'
        )

        session.add(videoData)

        session.commit()
        
        result = session.query(VideoData).count()
        expected = 1
        assert result == expected