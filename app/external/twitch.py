import json
import re
import requests

class TwitchVideo:
    def __init__(self, url):
        m = re.search('[0-9]{9}', url)
        self.video_id = m.group()

        with open('../config/config.json', 'r') as f:
            config = json.load(f)

        self.client_id = config['twitch']['client_id']
        self.client_secret = config['twitch']['client_secret']
        self.app_access_token = config['twitch']['app_access_token']


    def _get_token(self):
        with open('../config/config.json', 'r') as f:
            config = json.load(f)

        url = 'https://id.twitch.tv/oauth2/token'\
              '?client_id=' + self.client_id + \
              '&client_secret=' + self.client_secret + \
              '&grant_type=client_credentials'

        res = requests.post(url)
        print(res.text)
        res_text_dict = json.loads(res.text)

        config['twitch']['app_access_token'] = res_text_dict['access_token']

        # configのapp_access_tokenを更新する
        with open('../config/config.json', 'w') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        # インスタンス変数を更新する
        self.app_access_token = res_text_dict['access_token']


    #　この関数は例外を投げる（raise_for_status()）
    def get_info(self):
        url = 'https://api.twitch.tv/helix/videos?id=' + self.video_id
        headers = {
            'Authorization': 'Bearer ' + self.app_access_token,
            'Client-Id': self.client_id
        }
        res = requests.get(url, headers=headers)

        if res.status_code == 200:
            res_text_dict = json.loads(res.text)
            # 取得したdurationの単位を「分」に直す
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
        elif res.status_code == 401: # トークンの期限が切れていた場合の処理
            # トークンを再取得する
            self._get_token()

            headers = {
                'Authorization': 'Bearer ' + self.app_access_token,
                'Client-Id': self.client_id
            }
            res = requests.get(url, headers=headers)
            res_text_dict = json.loads(res.text)
            # 取得したdurationの単位を「分」に直す
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