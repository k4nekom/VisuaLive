import pytest

from apps.db import session
from videos.models import VideoData

@pytest.fixture(scope="function")
def testSession():
    yield session
    
    session.query(VideoData).delete()
    session.commit()