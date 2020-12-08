# import os
# os.environ['ENV'] = 'test'

from apps.db import Base, engine, session
from videos.models import VideoData

if __name__ == '__main__':
    Base.metadata.create_all(engine, checkfirst=True)