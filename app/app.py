import responder

api = responder.API()

@api.route("/")
def hello_world_html(req, resp):
    resp.html = api.template('index.html')

if __name__ == '__main__':
    api.run(port=5000, address='0.0.0.0')