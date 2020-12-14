from apps.db import session
from videos_data.models import VideoData
from videos_data.external import YoutubeVideo, TwitchVideo

class VideoDataService:
    def get_video_data(self, url, video_type):

        # dbに動画情報がある場合、そのデータを利用
        if session.query(VideoData).filter(VideoData.url==url).count() != 0:
            data = session.query(VideoData).filter(VideoData.url==url).one()
            video_data = {
                'user_name': data.username,
                'title': data.title,
                'broadcasted_at': data.broadcasted_at,
                'url': data.url,
                'channel_url': data.channel_url,
                'duration_minutes': data.duration_minutes,
                'comment_count': data.comment_count,
                'w_count': data.w_count
            }
        # dbに動画情報がない場合、externalパッケージを使い、外部から情報を取得してくる
        else:
            if video_type == 'twitch':
                video = TwitchVideo(url)
            elif video_type == 'youtube':
                video = YoutubeVideo(url)

            video_data = video.get_data()

            #　動画情報をDBへ保存
            data = VideoData(
                username = video_data['user_name'],
                title = video_data['title'],
                broadcasted_at = video_data['broadcasted_at'],
                url = video_data['url'],
                channel_url = video_data['channel_url'],
                duration_minutes = video_data['duration_minutes'],
                w_count = video_data['w_count'],
                comment_count = video_data['comment_count']
            )
            session.add(data)
            session.commit()

        return video_data

