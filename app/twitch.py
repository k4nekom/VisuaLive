class TwitchVideo:
    def __init__(self, url):
        self.video_id = url
        # jsonファイル開く
        self.client_id = None
        self.client_secret = None
        self.app_access_token = None

    # todo private化する
    def get_token(self):
        return self.video_id

    def get_info(self):
        return 'dict'
    
    def get_comments(self):
        return 'dict'