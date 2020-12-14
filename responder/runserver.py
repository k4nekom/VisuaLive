from apps.urls import api

# debug=Trueをつけてもデバッグモードにならないため
# uvicorn app:api --debug --port 5000 --host 0.0.0.0で起動する
if __name__ == '__main__':
    api.run(port=5000, address='0.0.0.0')