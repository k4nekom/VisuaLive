class VideoNotFound(Exception):
    """動画が見つからない（削除されているとき）に投げる例外"""
    pass
class ContinuationURLNotFound(Exception):
    pass

class LiveChatReplayDisabled(Exception):
    pass