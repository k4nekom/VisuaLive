import pytest

from twitch import TwitchVideo

@pytest.fixture()
def video():
    return TwitchVideo('https://www.twitch.tv/videos/739949384')

class TestTwitch:
    def test_get_token(self, video):
        video.get_token()
        assert type(video.app_access_token) is str

    def test_get_info(self, video):
        video.get_token()
        assert 'user_name' in video.get_info()

    def test_get_comments(self, video):
        video.get_token()
        assert 'comment_count' in video.get_comments