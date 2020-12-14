import pytest

from manage import api

@pytest.fixture()
def fixture_api():
    return api


def test_get(fixture_api):
    r = fixture_api.requests.get('/')
    assert r.status_code == 200
    assert '<div class="testHome"></div>' in r.text