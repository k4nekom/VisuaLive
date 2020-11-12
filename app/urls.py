from pathlib import Path

import responder

from external.twitch import TwitchVideo

BASE_DIR = Path(__file__).parent

api = responder.API(
    static_dir=str(BASE_DIR.joinpath('static')),
)

@api.route("/")
def home(req, resp):
    resp.html = api.template('home.html')

@api.route("/grapht")
async def grapth(req, resp):
    # todo urlが正しいかどうかのチェック
    request = await req.media()
    video = TwitchVideo(request['url'])
    resp.html = api.template('grapht.html', video_info=video.get_info(), comment_data=video.get_comment_data())
