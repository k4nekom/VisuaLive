from apps.app import api
from apps.base import ViewBase

class HomeView(ViewBase):
    async def on_get(self, req, resp):
        resp.html = api.template('homes/home.html', error_message=None)