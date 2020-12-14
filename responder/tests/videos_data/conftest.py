import pytest

from apps.db import session
from videos_data.models import VideoData

@pytest.fixture(scope="function")
def having_no_data_session():
    yield session
    
    session.query(VideoData).delete()
    session.commit()

# データがすでに登録されている場合のsession
@pytest.fixture(scope="function")
def having_data_session():
    twitch_data = VideoData(
        username = 'twitch',
        title = 'testだよ',
        broadcasted_at = '2020-09-13T14:15:18Z',
        url = 'https://www.twitch.tv/videos/739949384',
        channel_url = 'https://www.twitch.tv/videos/739949384',
        duration_minutes = 30,
        w_count = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        comment_count = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    )
    session.add(twitch_data)

    youtube_data = VideoData(
        username = 'youtube',
        title = 'testだよ',
        broadcasted_at = '2020-09-13T14:15:18Z',
        url = 'https://www.youtube.com/watch?v=iOavpCRbq-k',
        channel_url = 'https://www.youtube.com/watch?v=iOavpCRbq-k4',
        duration_minutes = 30,
        w_count = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        comment_count = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    )
    session.add(youtube_data)

    session.commit()

    yield session
    
    session.query(VideoData).delete()
    session.commit()