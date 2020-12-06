from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DATETIME

from apps.db import Base

class VideoData(Base):
    __tablename__ = 'video_data'
    id = Column('id', Integer, primary_key = True, autoincrement=True)
    username = Column('username', String(30), nullable=False)
    title = Column('title', String(50), nullable=False)
    broadcasted_at = Column('broadcasted_at', String(30), nullable=False)
    url = Column('url', String(255), unique=True, nullable=False)
    channel_url = Column('channel_url', String(255))
    duration_minutes = Column('duration_minutes', Integer, nullable=False)
    w_count = Column('w_count', Text, nullable=False)
    comment_count = Column('comment_count', Text, nullable=False)
    created_at = Column('created_at', DATETIME, nullable=False, default=datetime.now)
    updated_at = Column('updated_at', DATETIME, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __init__(self, username, title, broadcasted_at, url, channel_url, duration_minutes, w_count, comment_count):
        self.username = username
        self.title = title
        self.broadcasted_at = broadcasted_at
        self.url = url
        self.channel_url = channel_url
        self.duration_minutes = duration_minutes
        self.w_count = w_count
        self.comment_count = comment_count
        now = datetime.now()
        self.created_at = now
        self.updated_at = now


