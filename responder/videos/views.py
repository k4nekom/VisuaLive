import re

from apps.app import api, logger, set_logging
from apps.db import session
from videos.exceptions import VideoNotFound
from videos.external import TwitchVideo, TwitchVideoDemo, YoutubeVideo
from videos.models import VideoData

class CreateChartView:
    def __init__(self):
        set_logging()

    async def on_get(self, req, resp):
        resp.html = api.template('home.html', error_message=None)

    async def on_post(self, req, resp):
        request = await req.media()

        if session.query(VideoData).filter(VideoData.url==request['url']).count() == 0:

            if request['url'] == 'https://www.twitch.tv/videos/788601557':
                video = TwitchVideoDemo()
            elif re.fullmatch('https://www.twitch.tv/videos/\d{9}', request['url']) != None:
                video = TwitchVideo(request['url'])
            elif re.fullmatch('https://www.youtube.com/watch\?v=[0-9A-Za-z-_]{11}', request['url']) != None:
                video = YoutubeVideo(request['url'])
            else:
                resp.html = api.template('home.html', error_message='コメントの取得に失敗しました')
                return

            try:    
                video_info=video.get_info()
                comment_data=video.get_comment_data()
                videoDatun = VideoData(
                    username = video_info['user_name'],
                    title = video_info['title'],
                    broadcasted_at = video_info['created_at'],
                    url = video_info['url'],
                    channel_url = video_info['channel_url'],
                    duration_minutes = video_info['duration_minutes'],
                    w_count = comment_data['w_count'],
                    comment_count = comment_data['comment_count']
                )
                session.add(videoDatun)
                session.commit()
                resp.html = api.template('grapht.html', video_info=video_info, comment_data=comment_data)

            except VideoNotFound:
                logger.warning('catch VideoNotFound')
                resp.html = api.template('home.html', error_message='コメントの取得に失敗しました')


        else:
            videoDatum = session.query(VideoData).filter(VideoData.url==request['url']).one()

            video_info = {
                'user_name': videoDatum.username,
                'title': videoDatum.title,
                'created_at': videoDatum.broadcasted_at,
                'url': videoDatum.url,
                'channel_url': videoDatum.channel_url,
                'duration_minutes': videoDatum.duration_minutes
            }

            comment_data = {
                'comment_count': videoDatum.comment_count,
                'w_count': videoDatum.w_count
            }

            resp.html = api.template('grapht.html', video_info=video_info, comment_data=comment_data)
