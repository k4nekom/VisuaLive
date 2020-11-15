import pytest

from external.twitch_demo import TwitchVideoDemo

@pytest.fixture()
def video():
    return TwitchVideoDemo()

class TestTwitch:
    def test_get_info(self, video):
        video_info = video.get_info()
        assert 'user_name' in video_info
        assert 'title' in video_info
        assert 'created_at' in video_info
        assert 'url' in video_info
        assert 'duration_minutes' in video_info
        assert type(video_info['duration_minutes']) is int


    def test_get_comments(self, video):
        comment_data = video.get_comment_data()
        assert comment_data['comment_count'][0] == 64
        assert comment_data['w_count'][1] == 7