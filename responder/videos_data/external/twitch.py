import json
import re
import requests

from .base import ExternalBase
from videos_data.exceptions import VideoNotFound

class TwitchVideo(ExternalBase):
    def __init__(self, url):
        m = re.search('[0-9]{9}', url)
        self.video_id = m.group()

        with open('config/external.json', 'r') as f:
            config = json.load(f)

        self.client_id = config['twitch']['client_id']
        self.client_secret = config['twitch']['client_secret']
        self.app_access_token = config['twitch']['app_access_token']

        
    def get_data(self):
        video_info = self._get_info()
        video_comment_data = self._get_comment_data()
        video_data = {
            'user_name': video_info['user_name'],
            'title': video_info['title'],
            'broadcasted_at': video_info['created_at'],
            'url': video_info['url'],
            'channel_url': video_info['channel_url'],
            'duration_minutes': video_info['duration_minutes'],
            'w_count': video_comment_data['w_count'],
            'comment_count': video_comment_data['comment_count']
        }
        return video_data


    def _get_token(self):
        with open('config/external.json', 'r') as f:
            config = json.load(f)

        url = 'https://id.twitch.tv/oauth2/token'\
              '?client_id=' + self.client_id + \
              '&client_secret=' + self.client_secret + \
              '&grant_type=client_credentials'

        res = requests.post(url)
        res_text_dict = json.loads(res.text)

        config['twitch']['app_access_token'] = res_text_dict['access_token']

        # configのapp_access_tokenを更新する
        with open('config/external.json', 'w') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        # インスタンス変数を更新する
        self.app_access_token = res_text_dict['access_token']


    # このメソッドは例外投げます
    def _get_info(self):
        url = 'https://api.twitch.tv/helix/videos?id=' + self.video_id
        headers = {
            'Authorization': 'Bearer ' + self.app_access_token,
            'Client-Id': self.client_id
        }
        res = requests.get(url, headers=headers)

        if res.status_code == 401: # トークンの期限が切れていた場合、トークンを作り直し、再度リクエスト
            self._get_token()
            headers = {
                'Authorization': 'Bearer ' + self.app_access_token,
                'Client-Id': self.client_id
            }
            res = requests.get(url, headers=headers)

        if res.status_code !=200: # トークン再取得してもエラーの場合、例外を投げる
            raise(VideoNotFound('動画が公開期限切れ or 削除済'))

        res_text_dict = json.loads(res.text)
        # 取得したdurationの単位を「分」に直す
        duration_list = re.split('h|m|s', res_text_dict['data'][0]['duration'])
        duration_minutes = int(duration_list[0]) * 60 + int(duration_list[1]) + 1
        video_info = {
            'user_name': res_text_dict['data'][0]['user_name'],
            'title': res_text_dict['data'][0]['title'],
            'created_at': res_text_dict['data'][0]['created_at'],
            'url': res_text_dict['data'][0]['url'],
            'channel_url': 'https://www.twitch.tv/' + res_text_dict['data'][0]['user_name'],
            'duration_minutes': duration_minutes
        }
        return video_info
            
    
    def _get_comment_data(self):
        comments = []
        
        # 一回目のコメント取得リクエスト
        url = 'https://api.twitch.tv/v5/videos/' + self.video_id + '/comments?content_offset_seconds=0'
        headers = {'client-id': self.client_id}
        res = requests.get(url, headers=headers)
        res_dict = json.loads(res.text)
            
        for comment in res_dict['comments']:
            comments.append({
                'body': comment['message']['body'],
                'commented_minutes': int(comment['content_offset_seconds']) // 60
            })

        # 二回目以降のコメント取得リクエスト
        while '_next' in res_dict:
            url = 'https://api.twitch.tv/v5/videos/' + self.video_id + '/comments?cursor=' + res_dict['_next']
            headers = {'client-id': self.client_id}
            res = requests.get(url, headers=headers)
            res_dict = json.loads(res.text)

            for comment in res_dict['comments']:
                comments.append({
                    'body': comment['message']['body'],
                    'commented_minutes': int(comment['content_offset_seconds']) // 60
                })

        # １分ごとの、コメント数、末尾がwのコメント数を数える
        duration_minutes = comments[-1]['commented_minutes'] + 1

        comment_count = [0] * duration_minutes
        w_count = [0] * duration_minutes

        for comment in comments:
            comment_count[comment['commented_minutes']] += 1

            if super().has_kusa(comment['body']):
                w_count[comment['commented_minutes']] += 1

        comments_data = {
            'comment_count': comment_count,
            'w_count': w_count
        }

        return comments_data

