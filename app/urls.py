import responder

from external.twitch import TwitchVideo

api = responder.API()

@api.route("/")
def home(req, resp):
    resp.html = api.template('home.html')

@api.route("/grapht")
async def grapth(req, resp):
    # todo urlが正しいかどうかのチェック
    request = await req.media()
    video = TwitchVideo(request['url'])
    resp.html = api.template('grapht.html', video_info=video.get_info(), comment_data=video.get_comment_data())
