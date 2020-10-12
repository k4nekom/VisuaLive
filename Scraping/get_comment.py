import requests
import json
from collections import OrderedDict

client_id = 'zfpe6zkbszk1hez9g9hcxykn14ew4i'
video_id = ''

url = 'https://api.twitch.tv/v5/videos/764118280/comments?content_offset_seconds=0'
headers = {'client-id': client_id}
r = requests.get(url, headers=headers)
dict_data = r.json()

f = open("data.json", 'w')
with open ('data.json', 'w') as f:
    json.dump(dict_data, f, indent=4)

# 一回のリクエストで何件取得できる？取得件数？時間で区切る？

# リクエストの結果をCSV出力