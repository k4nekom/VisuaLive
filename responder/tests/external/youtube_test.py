import json

import pytest

from videos_data.external import YoutubeVideo
from videos_data.exceptions import VideoNotFound

@pytest.fixture()
def video():
    return YoutubeVideo('https://www.youtube.com/watch?v=iOavpCRbq-k')


class TestYoutube:
    def test_init(self, video):
        with open('config/external.json', 'r') as f:
            config = json.load(f)

        assert video.video_id == 'iOavpCRbq-k'
        assert video.api_key == config['youtube']['api_key']


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


    def test_failing_get_info(self, mocker, video):
        res_mock = mocker.Mock()
        res_mock.status_code = 200
        with open('tests/json/youtube_info_fail.json') as f:
            res_mock.text = f.read()

        mocker.patch('requests.get').return_value = res_mock

        with pytest.raises(VideoNotFound):
            video._get_info()


    # ------実際にクローリングをするテスト----------
    # def test_get_info_real_api(self, video):
    #     video_info = video._get_info()
    #     assert 'user_name' in video_info
    #     assert 'title' in video_info
    #     assert 'created_at' in video_info
    #     assert 'url' in video_info
    #     assert 'duration_minutes' in video_info
    #     assert type(video_info['duration_minutes']) is int
    # -----------------------------------------------------


    def test_get_comments(self, mocker, video):
        with open('tests/json/youtube_comment.json') as f:
            comments = json.loads(f.read())
        mocker.patch.object(YoutubeVideo, '_get_chat_replay_data', return_value = comments)

        comment_data = video._get_comment_data()
        assert type(comment_data['comment_count'][0]) is int
        assert type(comment_data['w_count'][0]) is int


    # ------実際にクローリングをするテスト----------
    # def test_get_comments_real_api(self):
    #     video = YoutubeVideo('https://www.youtube.com/watch?v=hjYmUjMaZAw')
    #     comment_data = video._get_comment_data()
    #     assert type(comment_data['comment_count'][0]) is int
    #     assert type(comment_data['w_count'][0]) is int
    # ------------------------------------------

    
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
