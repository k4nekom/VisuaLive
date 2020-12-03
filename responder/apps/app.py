from pathlib import Path

import responder

def create_app():
    BASE_DIR = Path(__file__).resolve().parents[2]

    api = responder.API(
        static_dir=str(BASE_DIR.joinpath('static')),
    )

    return api

api = create_app()
