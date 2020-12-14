import json

import pytest

from apps.app import logger
from apps.urls import api
from videos_data.external import YoutubeVideo
from videos_data.models import VideoData

@pytest.fixture()
def fixture_api():
    return api


def test_get_data_from_twitch(fixture_api, having_no_data_session, mocker):
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

    params = json.dumps({
        'url': 'https://www.twitch.tv/videos/739949384'
    })
    r = fixture_api.requests.post('/chart', params)
    assert r.status_code == 200
    assert '<div class="testGrapth"></div>' in r.text

    result = having_no_data_session.query(VideoData).count()
    expected = 1
    assert result == expected


def test_get_data_from_youtube(fixture_api, having_no_data_session, mocker):
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

    params = json.dumps({
        'url': 'https://www.youtube.com/watch?v=iOavpCRbq-k'
    })
    r = fixture_api.requests.post('/chart', params)

    assert r.status_code == 200
    assert '<div class="testGrapth"></div>' in r.text

    result = having_no_data_session.query(VideoData).count()
    expected = 1
    assert result == expected


def test_get_data_from_db(fixture_api, having_data_session, mocker):
    # 正常に動作するなら、request.get()は呼ばれないため、呼ばれたらエラーになるようにする
    mock = mocker.Mock()
    mock.status_code = 200
    mock.text = '{"error": "test faling"}'
    mocker.patch('requests.get').return_value = mock

    params = json.dumps({
        'url': 'https://www.youtube.com/watch?v=iOavpCRbq-k'
    })
    r = fixture_api.requests.post('/chart', params)
    assert r.status_code == 200
    assert '<div class="testGrapth"></div>' in r.text

    result = having_data_session.query(VideoData).count()
    expected = 2
    assert result == expected


@pytest.mark.parametrize(
    'url',
    [
        ('https://www.twitch.tv/videos/1234567890'),
        ('https://www.twitch.tv/videos/12345678'),
        ('https://www.twitch.tv/videos/12345678a'),
        ('https://www.twitch.tv/videos/000000000'),
        ('https://www.youtube.com/watch?v=hjYmUjMaZA'),
        ('https://www.youtube.com/watch?v=hjYmUjMaZAa'),
        ('https://www.youtube.com/watch?v=hjYmUjMaZ@')
    ]
)
def test_post_with_invalid_url(fixture_api, url):
    params = json.dumps({
        'url': url
    })
    r = fixture_api.requests.post('/chart', params)
    assert r.status_code == 200
    assert '<div class="testHome"></div>' in r.text
