import json

import pytest

from manage import api
from videos.external import YoutubeVideo

@pytest.fixture()
def api_fixture():
    return api


def test_root_get(api_fixture):
    r = api.requests.get('/')
    assert r.status_code == 200


def test_root_post_twitch(api_fixture, mocker):
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
                                                    get_info_mock,
                                                    with_next_mock, 
                                                    without_next_mock
                                                ]

    params = json.dumps({
        'url': 'https://www.twitch.tv/videos/739949384'
    })
    r = api.requests.post('/', params)
    assert r.status_code == 200


def test_root_post_youtube(api_fixture, mocker):
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
    r = api.requests.post('/', params)
    assert r.status_code == 200


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
def test_root_post_with_invalid_url(api_fixture, mocker, url):
    params = json.dumps({
        'url': url
    })
    r = api.requests.post('/', params)
    assert r.status_code == 200
