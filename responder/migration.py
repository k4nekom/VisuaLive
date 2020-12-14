import os

from apps.db import Base, engine, session
from videos_data.models import VideoData

if __name__ == '__main__':
    Base.metadata.create_all(engine, checkfirst=True)
    os.environ['ENV'] = 'test'
    Base.metadata.create_all(engine, checkfirst=True)