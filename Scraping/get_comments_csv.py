import requests
import json
import csv

client_id = 'zfpe6zkbszk1hez9g9hcxykn14ew4i'
video_id = '761262980'
index_count = 0
# 一回目のリクエスト
url = 'https://api.twitch.tv/v5/videos/' + video_id + '/comments?content_offset_seconds=0'
headers = {'client-id': client_id}
r = requests.get(url, headers=headers)
row_data = r.json()
    
with open('csv/extracted_data.csv', 'a') as f:
    writer = csv.writer(f)
    for comment in row_data['comments']:
        writer.writerow([
            index_count, 
            comment['content_offset_seconds'],
            comment['message']['body'],
            'emoticons' in comment['message']
        ])
        index_count += 1

# 二回目以降のリクエスト
while '_next' in row_data:
    url = 'https://api.twitch.tv/v5/videos/' + video_id + '/comments?cursor=' + row_data['_next']
    headers = {'client-id': client_id}
    r = requests.get(url, headers=headers)
    row_data = r.json()

    with open('csv/extracted_data.csv', 'a') as f:
        writer = csv.writer(f)
        for comment in row_data['comments']:
            writer.writerow([
                index_count, 
                comment['content_offset_seconds'],
                comment['message']['body'],
                'emoticons' in comment['message']
            ])
            index_count += 1

# 最後にrow_dataを出力する処理
# コメント取得完了 or エラー　を判定するため
with open ('json/error_row_data.json', 'w') as f:
    json.dump(row_data, f, indent=4)