import re
from pathlib import Path

import responder

from exception import VideoNotFoundError
from external.twitch import TwitchVideo
from external.twitch_demo import TwitchVideoDemo

BASE_DIR = Path(__file__).parent

api = responder.API(
    static_dir=str(BASE_DIR.joinpath('static')),
)

@api.route("/")
class root:
    async def on_get(self, req, resp):
        resp.html = api.template('home.html', error_message=None)

    async def on_post(self, req, resp):
        request = await req.media()

        if request['url'] == 'https://www.twitch.tv/videos/788601557':
            video = TwitchVideoDemo()
        elif re.fullmatch('https://www.twitch.tv/videos/\d{9}', request['url']) != None:
            video = TwitchVideo(request['url'])
        else:
            resp.html = api.template('home.html', error_message='動画のURLが無効です')
            return
            
        try:    
            resp.html = api.template('grapht.html', video_info=video.get_info(), comment_data=video.get_comment_data())
        except VideoNotFoundError as e:
            print('catch VideoNotFoundError:', e)
            resp.html = api.template('home.html', error_message='動画のURLが無効です')