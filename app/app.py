import responder

api = responder.API()

@api.route("/")
def home(req, resp):
    resp.html = api.template('home.html')

@api.route("/grapht")
def grapth(req, resp):
    resp.html = api.template('grapht.html', url=req.params['url'])

    
if __name__ == '__main__':
    api.run(port=5000, address='0.0.0.0')