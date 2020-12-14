from apps.app import api

from homes.views import HomeView
from videos_data.views import CreateChartView

api.add_route("/", HomeView)
api.add_route("/chart", CreateChartView)