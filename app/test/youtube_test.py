import json

import pytest

from external.youtube import YoutubeVideo
from exception import VideoNotFoundError

@pytest.fixture()
def video():
    return YoutubeVideo('https://www.youtube.com/watch?v=iOavpCRbq-k')


class TestYoutube:
    def test_init(self, video):
        with open('config/config.json', 'r') as f:
            config = json.load(f)

        assert video.video_id == 'iOavpCRbq-k'
        assert video.api_key == config['youtube']['api_key']


    # def test_get_info(self, mocker, video):
    #     res_mock = mocker.Mock()
    #     res_mock.status_code = 200
    #     with open('test/json/youtube_info.json') as f:
    #         res_mock.text = f.read()

    #     mocker.patch('requests.get').return_value = res_mock

    #     video_info = video.get_info()
    #     assert 'user_name' in video_info
    #     assert 'title' in video_info
    #     assert 'created_at' in video_info
    #     assert 'url' in video_info
    #     assert 'duration_minutes' in video_info
    #     assert type(video_info['duration_minutes']) is int


    # ------実際にtwitch apiを叩くテスト----------
    # def test_get_info_real_api(self, video):
    #     video_info = video.get_info()
    #     assert 'user_name' in video_info
    #     assert 'title' in video_info
    #     assert 'created_at' in video_info
    #     assert 'url' in video_info
    #     assert 'duration_minutes' in video_info
    #     assert type(video_info['duration_minutes']) is int
    # -----------------------------------------------------


    # def test_get_comments(self, mocker, video):
    #     # 動画情報取得のモック
    #     get_info_mock = mocker.Mock()
    #     get_info_mock.status_code = 200
    #     with open('test/json/video_info.json') as f:
    #         get_info_mock.text = f.read()
    #     # コメント取得のモック(_nextあり)
    #     with_next_mock = mocker.Mock()
    #     with_next_mock.status_code = 200
    #     with open('test/json/twitch_comment_with_next.json') as f:
    #         with_next_mock.text = f.read()
    #     # コメント取得のモック（_nextなし）
    #     without_next_mock = mocker.Mock()
    #     without_next_mock.status_code = 200
    #     with open('test/json/twitch_comment_without_next.json') as f:
    #         without_next_mock.text = f.read()

    #     mocker.patch('requests.get').side_effect = [get_info_mock, with_next_mock, without_next_mock]

    #     comment_data = video.get_comment_data()
    #     assert sum(comment_data['comment_count']) == 84
    #     assert type(comment_data['w_count'][0]) is int


    # ------実際にtwitch apiを叩くテスト----------
    # def test_get_comments_real_api(self, video):
    #     comment_data = video.get_comment_data()
    #     assert sum(comment_data['comment_count']) == 84
    #     assert type(comment_data['w_count'][0]) is int
    # ------------------------------------------
