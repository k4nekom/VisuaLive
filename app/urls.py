import re
from pathlib import Path

import responder

from exception import VideoNotFoundError
from external.twitch import TwitchVideo

BASE_DIR = Path(__file__).parent

api = responder.API(
    static_dir=str(BASE_DIR.joinpath('static')),
)

@api.route("/")
async def root(req, resp):
    if req.method == 'get':
        resp.html = api.template('home.html', error_message=None)
    elif req.method == 'post':
        request = await req.media()
        if re.fullmatch('https://www.twitch.tv/videos/\d{9}', request['url']) == None:
            resp.html = api.template('home.html', error_message='動画のURLが無効です')
        else:
            video = TwitchVideo(request['url'])
            try:    
                resp.html = api.template('grapht.html', video_info=video.get_info(), comment_data=video.get_comment_data())
            except VideoNotFoundError as e:
                print('catch VideoNotFoundError:', e)
                resp.html = api.template('home.html', error_message='動画のURLが無効です')