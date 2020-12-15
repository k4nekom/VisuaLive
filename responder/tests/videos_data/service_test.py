import json

import pytest

from videos_data.service import VideoDataService
from videos_data.models import VideoData
from videos_data.external import YoutubeVideo

@pytest.fixture()
def service():
    return VideoDataService()


# --------------- get_video_dataのテスト　-------------------------

# twitchから動画情報を取得する場合のテスト
class TestGetDataFromTwitch:
    # twitchから動画情報を取得し、正しく加工できているかのテスト
    def test_get_data(self, service, having_no_data_session, mocker):
        # 動画情報取得のモック
        get_info_mock = mocker.Mock()
        get_info_mock.status_code = 200
        with open('tests/json/video_info.json') as f:
            get_info_mock.text = f.read()
        # コメント取得のモック(_nextあり)
        with_next_mock = mocker.Mock()
        with_next_mock.status_code = 200
        with open('tests/json/twitch_comment_with_next.json') as f:
            with_next_mock.text = f.read()
        # コメント取得のモック（_nextなし）
        without_next_mock = mocker.Mock()
        without_next_mock.status_code = 200
        with open('tests/json/twitch_comment_without_next.json') as f:
            without_next_mock.text = f.read()

        mocker.patch('requests.get').side_effect = [
                                                        get_info_mock, 
                                                        with_next_mock, 
                                                        without_next_mock
                                                    ]

        url = 'https://www.twitch.tv/videos/739949384'
        video_type = 'twitch'
        video_data = service.get_video_data(url, video_type)

        assert 'user_name' in video_data
        assert 'title' in video_data
        assert 'broadcasted_at' in video_data
        assert 'url' in video_data
        assert 'channel_url' in video_data
        assert 'duration_minutes' in video_data
        assert 'comment_count' in video_data
        assert 'w_count' in video_data

    # twitchから取得した動画情報が、DBに保存できているかのテスト
    def test_save_data(self, service, having_no_data_session, mocker):
        # 動画情報取得のモック
        get_info_mock = mocker.Mock()
        get_info_mock.status_code = 200
        with open('tests/json/video_info.json') as f:
            get_info_mock.text = f.read()
        # コメント取得のモック(_nextあり)
        with_next_mock = mocker.Mock()
        with_next_mock.status_code = 200
        with open('tests/json/twitch_comment_with_next.json') as f:
            with_next_mock.text = f.read()
        # コメント取得のモック（_nextなし）
        without_next_mock = mocker.Mock()
        without_next_mock.status_code = 200
        with open('tests/json/twitch_comment_without_next.json') as f:
            without_next_mock.text = f.read()

        mocker.patch('requests.get').side_effect = [
                                                        get_info_mock, 
                                                        with_next_mock, 
                                                        without_next_mock
                                                    ]

        url = 'https://www.twitch.tv/videos/739949384'
        video_type = 'twitch'
        video_data = service.get_video_data(url, video_type)

        result = having_no_data_session.query(VideoData).count()
        expected = 1
        assert result == expected


# youtubeから動画情報を取得する場合のテスト
class TestGEtDataFromYoutube:
    # youtubeから動画情報を取得し、正しく加工できているかのテスト
    def test_get_data(self, service, having_no_data_session, mocker):
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

        url = 'https://www.youtube.com/watch?v=iOavpCRbq-k'
        video_type = 'youtube'
        video_data = service.get_video_data(url, video_type)

        assert 'user_name' in video_data
        assert 'title' in video_data
        assert 'broadcasted_at' in video_data
        assert 'url' in video_data
        assert 'channel_url' in video_data
        assert 'duration_minutes' in video_data
        assert 'comment_count' in video_data
        assert 'w_count' in video_data


    # youtubeから取得した動画情報が、DBに保存できているかのテスト
    def test_save_data(self, service, having_no_data_session, mocker):
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

        url = 'https://www.youtube.com/watch?v=iOavpCRbq-k'
        video_type = 'youtube'
        service.get_video_data(url, video_type)

        result = having_no_data_session.query(VideoData).count()
        expected = 1
        assert result == expected


# DBから動画情報を取得する場合のテスト
class TestGetDataFromDb:
    # DBから動画情報を取得し、正しく加工できているかのテスト
    def test_get_data(self, service, having_data_session, mocker):
        url = 'https://www.youtube.com/watch?v=iOavpCRbq-k'
        video_type = 'youtube'
        video_data = service.get_video_data(url, video_type)

        assert 'user_name' in video_data
        assert 'title' in video_data
        assert 'broadcasted_at' in video_data
        assert 'url' in video_data
        assert 'channel_url' in video_data
        assert 'duration_minutes' in video_data
        assert 'comment_count' in video_data
        assert 'w_count' in video_data


    # DBのレコード数が変化していないかのテスト（DBの値を取り出すだけなので変化なしが正常）
    def test_db_not_changed(self, service, having_data_session, mocker):
        url = 'https://www.youtube.com/watch?v=iOavpCRbq-k'
        video_type = 'youtube'
        service.get_video_data(url, video_type)

        result = having_data_session.query(VideoData).count()
        expected = 2
        assert result == expected

# --------------- get_video_dataのテスト終了　-------------------------
