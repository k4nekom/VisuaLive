import json

import pytest


from twitch import TwitchVideo

@pytest.fixture()
def video():
    return TwitchVideo('https://www.twitch.tv/videos/739949384')

class TestTwitch:
    def test_init(self, video):
        with open('config.json', 'r') as f:
            config = json.load(f)

        assert video.video_id == '739949384'
        assert video.client_id == config['twitch']['client_id']
        assert video.client_secret == config['twitch']['client_secret']
        assert video.app_access_token == config['twitch']['app_access_token']

    # mockを使ったテスト
    def test_get_info(self, mocker, video):
        responseMock = mocker.Mock()
        responseMock.status_code = 200
        with open('get_info.json') as f:
            responseMock.text = f.read()

        mocker.patch('requests.get').return_value = responseMock

        video_info = video.get_info()
        assert 'user_name' in video_info
        assert 'title' in video_info
        assert 'created_at' in video_info
        assert 'url' in video_info
        assert 'duration_minutes' in video_info
        assert type(video_info['duration_minutes']) is int

    # 実際にtwitch apiを叩くテスト
    # def test_get_info(self, video):
    #     video_info = video.get_info()
    #     assert 'user_name' in video_info
    #     assert 'title' in video_info
    #     assert 'created_at' in video_info
    #     assert 'url' in video_info
    #     assert 'duration_minutes' in video_info
    #     assert type(video_info['duration_minutes']) is int

    # mockを使ったテスト
    def test_get_info_with_invalid_token(self):
        with open('config.json', 'r') as f:
            config = json.load(f)
        app_access_tokne = config['twitch']['app_access_token']
        config['twitch']['app_access_token'] = '' # tokenがない場合をテストするためからにする

        with open('data/dst/test_new_update.json', 'w') as f:
            json.dump(d_update, f, indent=2, ensure_ascii=False)

        assert video.app_access_token == config['twitch']['app_access_token']

    # todo 実際にtwitch apiを叩くテスト
    # def test_get_info_with_invalid_token(self):




    # def test_get_token(self, video):
    #     video.get_token()
    #     assert type(video.app_access_token) is str

    # def test_get_comments(self, video):
    #     video.get_token()
    #     assert 'comment_count' in video.get_comments