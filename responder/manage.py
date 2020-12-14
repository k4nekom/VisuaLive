from apps.app import api

from homes.views import HomeView
from videos_data.views import CreateChartView

api.add_route("/", HomeView)
api.add_route("/chart", CreateChartView)

# debug=Trueをつけてもデバッグモードにならないため
# uvicorn app:api --debug --port 5000 --host 0.0.0.0で起動する
if __name__ == '__main__':
    api.run(port=5000, address='0.0.0.0')