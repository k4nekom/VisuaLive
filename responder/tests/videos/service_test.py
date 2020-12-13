import json

import pytest

from videos.service import VideoDataService
from videos.models import VideoData
from videos.external import YoutubeVideo

@pytest.fixture()
def service():
    return VideoDataService()


def test_get_data_from_twitch(service, having_no_data_session, mocker):
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

    result = having_no_data_session.query(VideoData).count()
    expected = 1
    assert result == expected


def test_get_data_from_youtube(service, having_no_data_session, mocker):
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

    result = having_no_data_session.query(VideoData).count()
    expected = 1
    assert result == expected


# 動画の情報がすでにDBに保存されていた場合のテスト
def test_get_data_from_db(service, having_data_session, mocker):
    # 正常に動作するなら、request.get()は呼ばれないため、呼ばれたらエラーになるようにする
    mock = mocker.Mock()
    mock.status_code = 200
    mock.text = '{"error": "test faling"}'
    mocker.patch('requests.get').return_value = mock

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

    result = having_data_session.query(VideoData).count()
    expected = 2
    assert result == expected