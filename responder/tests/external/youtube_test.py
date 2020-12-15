import json

import pytest

from videos_data.external import YoutubeVideo
from videos_data.exceptions import VideoNotFound

@pytest.fixture()
def video():
    return YoutubeVideo('https://www.youtube.com/watch?v=iOavpCRbq-k')


class TestInit:
    def test_init(self, video):
        with open('config/external.json', 'r') as f:
            config = json.load(f)

        assert video.video_id == 'iOavpCRbq-k'
        assert video.api_key == config['youtube']['api_key']


class TestGetInfo:
    # youtbue apiから動画情報を取得し、動画情報が正しく加工できているかのテスト
    def test_get_info(self, mocker, video):
        res_mock = mocker.Mock()
        res_mock.status_code = 200
        with open('tests/json/youtube_info.json') as f:
            res_mock.text = f.read()

        mocker.patch('requests.get').return_value = res_mock

        video_info = video._get_info()
        assert 'user_name' in video_info
        assert 'title' in video_info
        assert 'created_at' in video_info
        assert 'url' in video_info
        assert video_info['channel_url'] == 'https://www.youtube.com/channel/UC3lNFeJiTq6L3UWoz4g1e-A'
        assert 'duration_minutes' in video_info
        assert type(video_info['duration_minutes']) is int

    # youtube apiからの動画情報の取得に失敗した場合のテスト
    def test_failing_get_info(self, mocker, video):
        res_mock = mocker.Mock()
        res_mock.status_code = 200
        with open('tests/json/youtube_info_fail.json') as f:
            res_mock.text = f.read()

        mocker.patch('requests.get').return_value = res_mock

        with pytest.raises(VideoNotFound):
            video._get_info()


    # mockを使わずに、youtbue apiから動画情報を取得し、動画情報が正しく加工できているかのテスト
    # def test_get_info_real_api(self, video):
    #     video_info = video._get_info()
    #     assert 'user_name' in video_info
    #     assert 'title' in video_info
    #     assert 'created_at' in video_info
    #     assert 'url' in video_info
    #     assert 'duration_minutes' in video_info
    #     assert type(video_info['duration_minutes']) is int


class TestGetCommentData:
    # 動画コメントを取得し、コメントを正しく加工できているかのテスト
    def test_get_comment_data(self, mocker, video):
        with open('tests/json/youtube_comment.json') as f:
            comments = json.loads(f.read())
        mocker.patch.object(YoutubeVideo, '_get_chat_replay_data', return_value = comments)

        comment_data = video._get_comment_data()
        assert type(comment_data['comment_count'][0]) is int
        assert type(comment_data['w_count'][0]) is int


    # mockを使わずに動画コメントを取得し、コメントを正しく加工できているかのテスト
    # def test_get_comments_real_api(self):
    #     video = YoutubeVideo('https://www.youtube.com/watch?v=hjYmUjMaZAw')
    #     comment_data = video._get_comment_data()
    #     assert type(comment_data['comment_count'][0]) is int
    #     assert type(comment_data['w_count'][0]) is int


class GetData:
    def test_get_data(self, mocker, video):
        # 動画情報取得のモック
        res_mock = mocker.Mock()
        res_mock.status_code = 200
        with open('tests/json/youtube_info.json') as f:
            res_mock.text = f.read()
        mocker.patch('requests.get').return_value = res_mock

        # コメント取得のモック
        with open('tests/json/youtube_comment.json') as f:
            comments = json.loads(f.read())
        mocker.patch.object(YoutubeVideo, '_get_chat_replay_data', return_value = comments)

        video_data = video.get_data()
        assert 'user_name' in video_data
        assert 'title' in video_data
        assert 'broadcasted_at' in video_data
        assert 'url' in video_data
        assert 'channel_url' in video_data
        assert 'duration_minutes' in video_data
        assert 'comment_count' in video_data
        assert 'w_count' in video_data
