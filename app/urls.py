import responder

api = responder.API()

@api.route("/")
def home(req, resp):
    resp.html = api.template('home.html')

@api.route("/grapht")
async def grapth(req, resp):
    # todo urlが正しいかどうかのチェック
    request = await req.media()
    resp.html = api.template('grapht.html', url=request['url'])