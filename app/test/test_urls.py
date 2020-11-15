import os
import sys
import json

import pytest

sys.path.append('../')
from urls import api

os.chdir('../')

@pytest.fixture()
def api_fixture():
    return api

def test_root_get(api_fixture):
    r = api.requests.get('/')
    assert r.status_code == 200

def test_root_post(api_fixture, mocker):
    # 動画情報取得のモック
    get_info_mock = mocker.Mock()
    get_info_mock.status_code = 200
    with open('test/json/video_info.json') as f:
        get_info_mock.text = f.read()
    # コメント取得のモック(_nextあり)
    with_next_mock = mocker.Mock()
    with_next_mock.status_code = 200
    with open('test/json/twitch_comment_with_next.json') as f:
        with_next_mock.text = f.read()
    # コメント取得のモック（_nextなし）
    without_next_mock = mocker.Mock()
    without_next_mock.status_code = 200
    with open('test/json/twitch_comment_without_next.json') as f:
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

@pytest.mark.parametrize(
    'url',
    [
        ('https://www.twitch.tv/videos/1234567890'),
        ('https://www.twitch.tv/videos/12345678'),
        ('https://www.twitch.tv/videos/12345678a'),
        ('https://www.twitch.tv/videos/000000000')
    ]
)
def test_root_post_with_invalid_url(api_fixture, mocker, url):
    params = json.dumps({
        'url': url
    })
    r = api.requests.post('/', params)
    assert r.status_code == 200


def test_help(api_fixture):
    r = api.requests.get('/help')
    assert r.status_code == 200