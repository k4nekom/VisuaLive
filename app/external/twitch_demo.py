import json

from external.video import Video

class TwitchVideoDemo(Video):
    def get_info(self):
        with open('demo/info.json', 'r') as f:
            video_info = json.load(f)
        return video_info
            
    
    def get_comment_data(self):
        with open('demo/comment_data.json', 'r') as f:
            comment_data = json.load(f)        
        return comment_data