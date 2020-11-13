import os
import sys
import json
import re

sys.path.append('../')
from external.twitch import TwitchVideo

os.chdir('../')

url = 'https://www.twitch.tv/videos/788601557'
if re.fullmatch('https://www.twitch.tv/videos/\d{9}', url) == None:
    print('urlが間違っている')
else:
    video = TwitchVideo(url)

    video_info = video.get_info()
    with open ('demo_data/info.json', 'w') as f:
        json.dump(video_info, f, indent=4)

    comment_data = video.get_comment_data()
    with open ('demo_data/comment_data.json', 'w') as f:
        json.dump(comment_data, f, indent=4)