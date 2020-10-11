client_id = 'zfpe6zkbszk1hez9g9hcxykn14ew4i'
video_id = ''

# httpリクエストを送信
import requests
r = requests.get('https://api.twitch.tv/v5/videos/764118280/comments?content_offset_seconds=0')
print(r.json())
# 一回のリクエストで何件取得できる？取得件数？時間で区切る？

# リクエストの結果をCSV出力