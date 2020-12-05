import re

from apps.app import api
from videos.exceptions import VideoNotFoundError
from videos.external import TwitchVideo, TwitchVideoDemo, YoutubeVideo


class CreateChartView:
    async def on_get(self, req, resp):
        resp.html = api.template('home.html', error_message=None)

    async def on_post(self, req, resp):
        request = await req.media()

        if request['url'] == 'https://www.twitch.tv/videos/788601557':
            video = TwitchVideoDemo()
        elif re.fullmatch('https://www.twitch.tv/videos/\d{9}', request['url']) != None:
            video = TwitchVideo(request['url'])
        elif re.fullmatch('https://www.youtube.com/watch\?v=[0-9A-Za-z-_]{11}', request['url']) != None:
            video = YoutubeVideo(request['url'])
        else:
            resp.html = api.template('home.html', error_message='動画のURLが無効です')
            return

        try:    
            resp.html = api.template('grapht.html', video_info=video.get_info(), comment_data=video.get_comment_data())
        except VideoNotFoundError as e:
            print('catch VideoNotFoundError:', e)
            resp.html = api.template('home.html', error_message='動画のURLが無効です')