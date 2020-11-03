import json
import re
import requests

class TwitchVideo:
    def __init__(self, url):
        m = re.search('[0-9]{9}', url)
        self.video_id = m.group()

        with open('config.json', 'r') as f:
            config = json.load(f)

        self.client_id = config['twitch']['client_id']
        self.client_secret = config['twitch']['client_secret']
        self.app_access_token = config['twitch']['app_access_token']

    # todo private化する
    def get_token(self):
        
        return self.video_id

    def get_info(self):

        url = 'https://api.twitch.tv/helix/videos?id=' + self.video_id
        headers = {
            'Authorization': 'Bearer ' + self.app_access_token,
            'Client-Id': self.client_id
        }
        res = requests.get(url, headers=headers)
        res_text_dict = json.loads(res.text)

        duration_list = re.split('h|m|s', res_text_dict['data'][0]['duration'])
        duration_minutes = int(duration_list[0]) * 60 + int(duration_list[1]) + 1

        video_info = {
            'user_name': res_text_dict['data'][0]['user_name'],
            'title': res_text_dict['data'][0]['title'],
            'created_at': res_text_dict['data'][0]['created_at'],
            'url': res_text_dict['data'][0]['url'],
            'duration_minutes': duration_minutes
        }

        return video_info
    
    def get_comments(self):
        return 'dict'